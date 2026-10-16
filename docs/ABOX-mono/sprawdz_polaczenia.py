#!/usr/bin/env python3
"""Compare the rendered wire graph with an independently declared netlist.

Coordinates are quantized to 1e-6 drawing units. A four-way crossing joins
only when a recorded endpoint, component pin, label or junction is present.
This checks exported connectivity, not electrical ratings or simulation.
"""

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import sys


SCALE = 1_000_000


class DisjointSet:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def add(self, point):
        if point not in self.parent:
            self.parent[point] = point
            self.rank[point] = 0

    def find(self, point):
        parent = self.parent[point]
        if parent != point:
            self.parent[point] = self.find(parent)
        return self.parent[point]

    def union(self, first, second):
        first, second = self.find(first), self.find(second)
        if first == second:
            return
        if self.rank[first] < self.rank[second]:
            first, second = second, first
        self.parent[second] = first
        if self.rank[first] == self.rank[second]:
            self.rank[first] += 1


def point(value, description):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{description}: wymagane dwie współrzędne")
    if any(isinstance(v, bool) or not isinstance(v, (int, float))
           or not math.isfinite(v) for v in value):
        raise ValueError(f"{description}: nieprawidłowe współrzędne")
    return tuple(round(v * SCALE) for v in value)


def lies_on(p, segment):
    (x1, y1), (x2, y2) = segment
    x, y = p
    if y1 == y2:
        return y == y1 and min(x1, x2) <= x <= max(x1, x2)
    return x == x1 and min(y1, y2) <= y <= max(y1, y2)


def describe(items, limit=16):
    items = sorted(items)
    result = ", ".join(items[:limit])
    if len(items) > limit:
        result += f", … (+{len(items) - limit})"
    return result


def symbol_body(component, ref):
    """Infer supported symbol interiors from the renderer's public pins."""
    kind = component.get("kind")
    raw_pins = component.get("pins", {})
    if kind == "Q" and "B" in raw_pins:
        base = point(raw_pins["B"], f"Pin {ref}.B")
        return ("circle", (base[0] + round(2.5 * SCALE), base[1]),
                round(1.55 * SCALE))
    if kind not in {"R", "POT", "C"} or not {"1", "2"} <= set(raw_pins):
        return None
    first = point(raw_pins["1"], f"Pin {ref}.1")
    second = point(raw_pins["2"], f"Pin {ref}.2")
    if first == second or (first[0] != second[0] and first[1] != second[1]):
        return None
    center = ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2)
    along, perpendicular = ((0.35, 0.9) if kind == "C" else (1.4, 0.45))
    if first[1] == second[1]:
        half_x, half_y = along * SCALE, perpendicular * SCALE
    else:
        half_x, half_y = perpendicular * SCALE, along * SCALE
    return ("rectangle", (center[0] - half_x, center[1] - half_y,
                          center[0] + half_x, center[1] + half_y))


def crosses_symbol_interior(segment, body):
    """Boundary contact is allowed; entry by more than 1e-6 is not."""
    (x1, y1), (x2, y2) = segment
    if body[0] == "circle":
        (_, (cx, cy), radius) = body
        nearest_x = min(max(cx, min(x1, x2)), max(x1, x2))
        nearest_y = min(max(cy, min(y1, y2)), max(y1, y2))
        return ((nearest_x - cx) ** 2 + (nearest_y - cy) ** 2
                < (radius - 1) ** 2)
    left, bottom, right, top = body[1]
    if y1 == y2:
        return (bottom + 1 < y1 < top - 1
                and max(min(x1, x2), left + 1)
                < min(max(x1, x2), right - 1))
    return (left + 1 < x1 < right - 1
            and max(min(y1, y2), bottom + 1)
            < min(max(y1, y2), top - 1))


def drawing_collisions(components, segments):
    errors = []
    for ref, component in sorted(components.items()):
        body = symbol_body(component, ref)
        if body is None:
            continue
        hits = [segment for segment in segments
                if crosses_symbol_interior(segment, body)]
        if not hits:
            continue
        examples = []
        for first, second in hits[:3]:
            examples.append(f"({first[0] / SCALE:g}, {first[1] / SCALE:g})–"
                            f"({second[0] / SCALE:g}, {second[1] / SCALE:g})")
        suffix = f"; dalsze odcinki: {len(hits) - 3}" if len(hits) > 3 else ""
        errors.append(f"Kolizja graficzna z symbolem {ref}: przewód "
                      + "; ".join(examples) + suffix
                      + " (kolizja rysunku, nie rozstrzygnięcie zwarcia)")
    return errors


def check_connections(expected, geometry):
    """Return counts and errors; raise ValueError for malformed input."""
    if not isinstance(expected, dict) or not isinstance(geometry, dict):
        raise ValueError("Oba pliki muszą zawierać obiekty JSON")
    expected_components = expected.get("components")
    actual_components = geometry.get("components")
    if not isinstance(expected_components, dict):
        raise ValueError("Lista oczekiwana: brak obiektu components")
    if not isinstance(actual_components, dict):
        raise ValueError("Geometria: brak obiektu components")
    if not expected_components or not actual_components:
        raise ValueError("Lista elementów nie może być pusta")

    expected_pins = {}
    for ref, component in expected_components.items():
        if not isinstance(component, dict) or not isinstance(component.get("pins"), dict):
            raise ValueError(f"Lista oczekiwana: {ref} nie ma obiektu pins")
        if not component["pins"]:
            raise ValueError(f"Lista oczekiwana: {ref} nie ma pinów")
        for pin, net in component["pins"].items():
            if not isinstance(net, str) or not net:
                raise ValueError(f"Lista oczekiwana: {ref}.{pin} nie ma nazwy sieci")
            expected_pins[(ref, pin)] = net

    graph = DisjointSet()
    segments = []
    for index, raw_segment in enumerate(geometry.get("segments", [])):
        if not isinstance(raw_segment, (list, tuple)) or len(raw_segment) != 2:
            raise ValueError(f"Odcinek {index}: wymagane dwa końce")
        first = point(raw_segment[0], f"Odcinek {index}, początek")
        second = point(raw_segment[1], f"Odcinek {index}, koniec")
        if first[0] != second[0] and first[1] != second[1]:
            raise ValueError(f"Odcinek {index}: obsługiwane są odcinki poziome i pionowe")
        segments.append((first, second))
        graph.add(first)
        graph.add(second)

    actual_pins = {}
    pins_at_point = defaultdict(list)
    for ref, component in actual_components.items():
        if not isinstance(component, dict) or not isinstance(component.get("pins"), dict):
            raise ValueError(f"Geometria: {ref} nie ma obiektu pins")
        if not component["pins"]:
            raise ValueError(f"Geometria: {ref} nie ma pinów")
        for pin, raw_point in component["pins"].items():
            p = point(raw_point, f"Pin {ref}.{pin}")
            actual_pins[(ref, pin)] = p
            pins_at_point[p].append(f"{ref}.{pin}")
            graph.add(p)

    junctions = []
    for index, raw_point in enumerate(geometry.get("junctions", [])):
        p = point(raw_point, f"Węzeł {index}")
        graph.add(p)
        junctions.append(p)

    labels = []
    labels_at_point = defaultdict(list)
    for index, label in enumerate(geometry.get("labels", [])):
        if not isinstance(label, dict) or not isinstance(label.get("name"), str) or not label["name"]:
            raise ValueError(f"Etykieta {index}: brak nazwy")
        p = point(label.get("point"), f"Etykieta {label['name']}")
        labels.append((label["name"], p))
        labels_at_point[p].append(label["name"])
        graph.add(p)

    # All registered points lying on a wire join it. This also joins touching
    # endpoints, T junctions and collinear overlaps, without joining an ordinary
    # four-way crossing whose coordinate has never been registered.
    all_points = list(graph.parent)
    points_on_wires = set()
    for segment in segments:
        start = segment[0]
        for p in all_points:
            if lies_on(p, segment):
                graph.union(start, p)
                points_on_wires.add(p)

    collisions = drawing_collisions(actual_components, segments)
    errors = list(collisions)
    for name, p in labels:
        if p not in points_on_wires and p not in pins_at_point:
            errors.append(f"Niepodłączona etykieta {name} przy "
                          f"({p[0] / SCALE:g}, {p[1] / SCALE:g})")
    for (ref, pin), p in actual_pins.items():
        if (p not in points_on_wires and len(pins_at_point[p]) < 2
                and p not in labels_at_point):
            errors.append(f"Niepodłączony pin {ref}.{pin}")

    # Global names are electrical connections even when drawn remotely.
    label_roots = {}
    for name, p in labels:
        if name in label_roots:
            graph.union(label_roots[name], p)
        else:
            label_roots[name] = p

    expected_refs = set(expected_components)
    actual_refs = set(actual_components)
    for ref in sorted(expected_refs - actual_refs):
        errors.append(f"Brak elementu {ref}")
    for ref in sorted(actual_refs - expected_refs):
        errors.append(f"Nadmiarowy element {ref}")
    for ref in sorted(expected_refs & actual_refs):
        wanted = set(expected_components[ref]["pins"])
        have = set(actual_components[ref]["pins"])
        for pin in sorted(wanted - have):
            errors.append(f"Brak pinu {ref}.{pin}")
        for pin in sorted(have - wanted):
            errors.append(f"Nadmiarowy pin {ref}.{pin}")

    # Compare the independently supplied net partition with physical roots.
    # Including names on labels catches a wrong label even if every component
    # in that branch is otherwise connected to its neighbours.
    members = defaultdict(lambda: defaultdict(list))
    nets_at_root = defaultdict(set)
    for key, net in expected_pins.items():
        if key not in actual_pins:
            continue
        root = graph.find(actual_pins[key])
        members[net][root].append(".".join(key))
        nets_at_root[root].add(net)
    for name, p in labels:
        root = graph.find(p)
        members[name][root].append(f"etykieta:{name}")
        nets_at_root[root].add(name)

    for net in sorted(members):
        groups = members[net]
        if len(groups) > 1:
            descriptions = [describe(group) for group in groups.values()]
            errors.append(f"Przerwa w sieci {net}: " + " | ".join(descriptions))
    for root, nets in sorted(nets_at_root.items()):
        if len(nets) > 1:
            evidence = []
            for net in sorted(nets):
                evidence.append(f"{net}: {describe(members[net][root], 8)}")
            errors.append("Zwarcie różnych sieci: " + " | ".join(evidence))

    return {
        "components": len(actual_components),
        "pins": len(actual_pins),
        "segments": len(segments),
        "junctions": len(junctions),
        "labels": len(labels),
        "nets": len({graph.find(p) for p in actual_pins.values()}),
        "expected_nets": len(set(expected_pins.values())),
        "symbol_collisions": len(collisions),
        "errors": errors,
    }


def main():
    directory = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", nargs="?", type=Path,
                        default=directory / "polaczenia.json")
    parser.add_argument("geometry", nargs="?", type=Path,
                        default=directory / "schemat-geometria.json")
    args = parser.parse_args()
    try:
        expected = json.loads(args.expected.read_text(encoding="utf-8"))
        geometry = json.loads(args.geometry.read_text(encoding="utf-8"))
        result = check_connections(expected, geometry)
    except (OSError, ValueError, TypeError) as exc:
        print(f"BŁĄD danych wejściowych: {exc}", file=sys.stderr)
        return 2
    print(f"Sprawdzono: {result['components']} elementów, {result['pins']} pinów, "
          f"{result['segments']} odcinków, {result['junctions']} węzłów, "
          f"{result['labels']} etykiet.")
    print(f"Sieci przy pinach: {result['nets']}; oczekiwane: {result['expected_nets']}.")
    print(f"Kolizje przewodów z symbolami: {result['symbol_collisions']}.")
    for error in result["errors"]:
        print(f"BŁĄD: {error}")
    if result["errors"]:
        print(f"Niezgodności: {len(result['errors'])}.")
        return 1
    print("OK: połączenia zgadzają się z niezależną listą sieci.")
    print("Kontrola nie potwierdza parametrów elektrycznych ani stabilności wzmacniacza.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
