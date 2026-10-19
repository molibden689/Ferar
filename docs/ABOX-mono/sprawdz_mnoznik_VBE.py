"""DC estimates for the drawn VBE multiplier and positive cascode headroom.

This is not a SPICE, SOA, stability or transistor temperature model.
VBE and gain are explicit scenario assumptions, not manufacturer guarantees.
"""
import json
from pathlib import Path
import re

import numpy as np
from scipy.optimize import brentq

from sprawdz_T12_T16 import BETA_PRE, R20, VPK, load_line


ROOT = Path(__file__).resolve().parent


def resistance(components, ref):
    match = re.match(r"([0-9]+(?:[,.][0-9]+)?)\s*([kM]?)Ω", components[ref]["value"])
    if not match:
        raise ValueError(f"Cannot read resistance {ref}")
    return float(match[1].replace(",", ".")) * {"": 1, "k": 1000, "M": 1e6}[match[2]]


def multiplier(current, vbe, beta, rcb, rbe):
    divider_current = vbe / rbe
    ib = (current - divider_current) / (beta + 1)
    if ib <= 0:
        raise ValueError("Scenario does not sustain forward-active bias transistor")
    ic = beta * ib
    voltage = vbe * (1 + rcb / rbe) + rcb * ib
    # Balance physical currents at collector and base nodes.
    ircb = (voltage - vbe) / rcb
    residual = max(abs(current - ic - ircb), abs(ircb - divider_current - ib))
    if residual > 1e-12:
        raise AssertionError(f"Multiplier KCL residual {residual}")
    return voltage, residual


def required_vh(amplitude, impedance, beta_output, beta_driver, vbe=0.65):
    vout = np.array([amplitude])
    iout = vout / impedance
    ic12, _, _, active = load_line(vout, iout, 50, beta_output, beta_driver)
    if not bool(active[0]):
        raise ValueError("Outside active-branch approximation")
    ie12 = float(ic12[0]) * (1 + 1 / BETA_PRE)
    return amplitude + R20 * ie12 + 2 * vbe


def main():
    netlist = json.loads((ROOT / "polaczenia.json").read_text())
    components = netlist["components"]
    rcb, rfixed, pmax = (resistance(components, ref) for ref in ("R30", "R31", "P1"))
    current, vbe, beta = 0.003, 0.65, 100
    low, residual_low = multiplier(current, vbe, beta, rcb, rfixed + pmax)
    high, residual_high = multiplier(current, vbe, beta, rcb, rfixed)
    target = 2.85  # Illustrative voltage, NOT an approved idle current setting.
    pot_for_target = brentq(
        lambda p: multiplier(current, vbe, beta, rcb, rfixed + p)[0] - target,
        0, pmax)
    # Loss of wiper contact: the drawn strap retains the whole end-to-end track.
    wiper_open_voltage = multiplier(current, vbe, beta, rcb, rfixed + pmax)[0]
    if not (low < target < high and abs(wiper_open_voltage - low) < 1e-12):
        raise AssertionError("Adjustment direction or nominal range is wrong")

    # Illustrative corners, not tolerance specifications for an unspecified pot.
    corners = {"minimum_setting_V": [], "maximum_setting_V": []}
    max_kcl = max(residual_low, residual_high)
    for assumed_current in (0.0015, 0.003, 0.0035):
        for assumed_vbe in (0.60, 0.65, 0.72):
            for assumed_beta in (40, 100, 200):
                for tc in (0.99, 1.01):
                    for tb in (0.99, 1.01):
                        for tp in (0.8, 1.2):
                            for key, p in (("minimum_setting_V", pmax * tp),
                                           ("maximum_setting_V", 0)):
                                voltage, residual = multiplier(
                                    assumed_current, assumed_vbe, assumed_beta,
                                    rcb * tc, rfixed * tb + p)
                                corners[key].append(voltage)
                                max_kcl = max(max_kcl, residual)

    # R13 is the new explicit design choice, not an asserted source reading.
    vp, r14 = 40.0, resistance(components, "R14")
    r13_new = resistance(components, "R13")
    headroom = []
    for r13 in (8200.0, r13_new):
        # Ignore T8 base current: this is the unloaded divider estimate.
        vb8 = vp * r13 / (r13 + r14)
        ve8 = vb8 + vbe
        vec7 = vp - vbe - ve8
        for beta_output in (20, 40, 80):
            for beta_driver in (25, 40, 80):
                vh = required_vh(VPK, 6, beta_output, beta_driver)
                amp_1v = brentq(
                    lambda amp: ve8 - required_vh(amp, 6, beta_output, beta_driver) - 1,
                    1, 40)
                headroom.append({
                    "R13_ohm": r13, "regulated_positive_V": vp,
                    "beta_output_assumed": beta_output, "beta_driver_assumed": beta_driver,
                    "VB8_unloaded_V": vb8, "VE8_estimate_V": ve8,
                    "VEC7_estimate_V": vec7, "VH_required_100W_6ohm_V": vh,
                    "VEC8_at_100W_V": ve8 - vh,
                    "B_minus_C_T8_at_100W_V": vb8 - vh,
                    "illustrative_amplitude_with_1V_VEC8_V": amp_1v,
                    "illustrative_power_with_1V_VEC8_W": amp_1v**2 / 12,
                })

    result = {
        "limits": [
            "Not SPICE, SOA, measured bias, thermal transient or stability validation.",
            "Multiplier current and VBE/gain are assumptions; idle current is not solved.",
            "Cascode estimates use an unloaded divider and constant VBE=0.65 V.",
            "1 V VEC8 is an illustrative margin, not a manufacturer's distortion threshold.",
            "All headroom numbers assume the regulated rail is maintained under load."
        ],
        "multiplier": {
            "current_assumed_A": current, "VBE_assumed_V": vbe, "beta_assumed": beta,
            "R30_ohm": rcb, "R31_ohm": rfixed, "P1_max_ohm": pmax,
            "nominal_minimum_V": low, "nominal_maximum_V": high,
            "example_target_V": target, "P1_for_example_target_ohm": pot_for_target,
            "wiper_contact_lost_with_intact_strap_V": wiper_open_voltage,
            "illustrative_corner_ranges_V": {
                key: {"minimum": min(values), "maximum": max(values)}
                for key, values in corners.items()
            },
            "corner_assumptions": "I=1.5..3.5mA, VBE=.60..72V, beta40..200, fixedR±1%, pot±20%",
            "maximum_KCL_residual_A": max_kcl,
        },
        "positive_cascode": headroom,
    }
    (ROOT / "mnoznik-VBE-kontrola.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"Nominal multiplier range: {low:.4f} .. {high:.4f} V")
    print(f"P1 for illustrative {target} V: {pot_for_target:.2f} ohm")
    print(f"Multiplier maximum KCL residual: {max_kcl:.3g} A")
    for row in headroom:
        if row["beta_output_assumed"] == 20 and row["beta_driver_assumed"] == 25:
            print(f"R13={row['R13_ohm']:g} ohm: "
                  f"VEC8 at target {row['VEC8_at_100W_V']:.3f} V; "
                  f"power with illustrative 1 V margin "
                  f"{row['illustrative_power_with_1V_VEC8_W']:.2f} W")
    print("These checks do not establish idle current, stability or achieved power.")


if __name__ == "__main__":
    main()
