# Kontrola schematu z mnożnikiem VBE

Wersja z 19 października 2026 r. [Pełny schemat PNG](schemat.png), [PDF](schemat.pdf), [powiększenie mnożnika](mnoznik-VBE.png).

## Co zmieniono

- D4–D7 i Rc usunięto. D1–D3 pozostają w swoich dotychczasowych węzłach.
- Q19 = 2SC5171 NPN: C = VH, E = VL, B = VBIAS_B. Z dostarczonej karty wynika 1=B, 2=C, 3=E. Nie połączono go z masą.
- R30 = 3,3 kΩ między C–B; R31 = 820 Ω i P1 = 1 kΩ szeregowo między B–E. Suwak P1 zwarty z końcem od strony VL. START P1 = 1 kΩ.
- R13 = **12 kΩ / 1% / co najmniej 0,25 W** to nowy dobór dla ±40 V. Nie jest rzekomym potwierdzeniem nieczytelnej wartości oryginału.
- Ujednolicono wartości opisane na rysunku i w liście elementów: kondensatory szyn 470 µF / 100 V, C7/C8 25 V, C6 39 pF C0G / 100 V, C9 220 nF / 250 V, R25/R26 2,49 Ω / 2 W, R27 0,62 Ω / 5 W. Wcześniej JSON zachowywał część wartości źródłowych mimo nowszych opisów na rysunku.

Pozostałe połączenia wzmacniacza nie zmieniły sieci. Zachowano R12 do masy, pływający środek R17/R18, kolektory T13/T17 i powroty R20/R21 do OUTI oraz kolektory T11/T15 do osobnych szyn VP/VM. Zostaje jedna para końcowa T14 = 2SA1943 i T18 = 2SC5200. Plików odtworzenia oryginału nie zmieniono.

## Sprawdzenie połączeń

Nowy wariant: **67 elementów, 155 wyprowadzeń, 49 sieci**.

Geometrię przewodów porównano z listą oryginalnych połączeń i jawnymi zmianami modernizacji. Kontrola obejmuje brakujące piny i elementy, przerwy, zwarcia różnych sieci, etykiety i kolizje przewodów z symbolami. Wynik: brak zgłoszonych niezgodności i kolizji. Niezależny przegląd różnicy względem poprzedniego wariantu potwierdził, że pozostałe piny zachowały sieci. Obejrzano pełny rysunek i powiększenie Q19.

Lista połączeń: [polaczenia.json](polaczenia.json). Geometria: [schemat-geometria.json](schemat-geometria.json). Checker: [sprawdz_polaczenia.py](sprawdz_polaczenia.py). To kontrola grafu połączeń, nie ERC programu CAD ani weryfikacja działania elektrycznego. Checker nie porównuje automatycznie wartości; wymienione wyżej wartości sprawdzono w przeglądzie rysunku i listy.

## Mnożnik — obliczenia DC

Dla prądu dwójnika I = 3 mA, VBE19 = 0,65 V i β19 = 100:

```text
RBE = R31 + P1
IB19 = (I − VBE19/RBE) / (β19 + 1)
Vbias = VBE19 × (1 + R30/RBE) + R30 × IB19
```

Wyniki:

- P1 = 1 kΩ: Vbias ≈ 1,915 V — nominalne minimum;
- P1 = 0 Ω: Vbias ≈ 3,338 V — nominalne maksimum;
- przykład Vbias = 2,85 V: P1 ≈ 190 Ω, co nie jest nastawą uruchomieniową ani wyznaczeniem prądu jałowego;
- utrata kontaktu suwaka z nienaruszoną ścieżką i przewodem zwarcia pozostawia pełne 1 kΩ;
- maksymalna reszta bilansu prądów mnożnika poniżej 10⁻¹⁸ A w analizowanych przypadkach.

Sprawdzono też ilustracyjne skrajne założenia: I = 1,5–3,5 mA, VBE = 0,60–0,72 V, β = 40–200, rezystory ±1%, potencjometr ±20%. To scenariusze, nie gwarantowane parametry wybranych egzemplarzy. Przy maksymalnym P1 w niektórych scenariuszach wychodzi około 2,46 V; nie gwarantuje to zerowego IQ. Kontrola obejmuje model DC mnożnika, nie charakterystyki tranzystora producenta i nie pełny punkt pracy wzmacniacza.

## Dlaczego zmieniono R13

Dotychczasowe R13 = 8,2 kΩ i R14 = 820 Ω, przy VP = 40 V, dawały z nieobciążonego dzielnika VB8 ≈ 36,364 V i VE8 ≈ 37,014 V. Istniejący model wyjścia przy 100 W / 6 Ω i założonych β końcowego = 20 oraz drivera = 25 wymaga VH ≈ 37,378 V. W tym scenariuszu kolektor T8 byłby wyżej od emitera; przyjęta praca kaskody nie jest możliwa.

Nowe R13 = 12 kΩ daje VB8 ≈ 37,441 V i VE8 ≈ 38,091 V. Przy założonych spadkach 0,65 V na D3 i złączach otrzymujemy:

- VEC7 ≈ 1,259 V;
- w tym samym wymagającym scenariuszu VEC8 ≈ 0,713 V i VB8−VC8 ≈ 0,063 V;
- C7 pracuje przy spadku około 2,559 V;
- straty R13 wynoszą około 0,117 W, więc przyjęto co najmniej 0,25 W.

Prąd bazy PNP T8 podnosi napięcie dzielnika, ale nie jest uwzględniony w powyższych prostych liczbach. Przy przykładowym IB8 ≈ 40 µA zmiana jest rzędu 30 mV. Temperatura i rozrzut VBE również zmieniają marginesy.

Nowy dobór usuwa oczywistą sprzeczność nominalnego przykładu, ale nie daje gwarancji osiągnięcia 100 W z małymi zniekształceniami. Przy umownie wymaganym zapasie VEC8 ≥ 1 V model β = 20/25 wskazuje około **98,4 W**; dla starego 8,2 kΩ było około 92,5 W. Granica 1 V jest ilustracyjnym kryterium projektu, nie limitem zniekształceń podanym przez producenta. Wyniki przy innych założonych β zapisano w JSON. Na rysunku **100 W pozostaje celem**.

Obliczenia: [sprawdz_mnoznik_VBE.py](sprawdz_mnoznik_VBE.py), [wyniki](mnoznik-VBE-kontrola.json). Używają jawnych założeń i dotychczasowego modelu wyjścia. Nie są symulacją SPICE. Nie wyznaczają dopuszczalnego prądu przy zadanym SOA ani osiągniętej mocy.

## Co nadal wymaga weryfikacji

- Pełny punkt pracy z rzeczywistymi VBE(I,T) i β, docelowy IC spoczynkowy końcowych oraz nastawa P1. Prąd RE obejmuje także bocznik 68 Ω.
- Sprzężenie cieplne Q19 z T11/T12/T15/T16 i zachowanie IQ podczas nagrzewania różnych części. Nie zatwierdzono montażu czujnika wyłącznie na radiatorze końcowych.
- Kompensacja częstotliwościowa, stabilność, obciążenia reaktywne, gorące SOA i chłodzenie. Wartość C6 pozostaje robocza.
- Utrzymanie ±40 V pod obciążeniem, układy stabilizatorów, rozruch i zanik szyny.
- Zabezpieczenia prądowe, termiczne i głośnika przed DC. Rysunek nie jest projektem PCB; brak Gerberów i pomiarów prototypu.

Nie wykonano symulacji z modelami producentów ani pomiarów. Wynik kontroli oznacza zgodność połączeń oraz spójność opisanych obliczeń wstępnych, a nie zatwierdzenie wzmacniacza do uruchomienia.
