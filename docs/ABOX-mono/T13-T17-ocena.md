# T13 / T17 — wybrane sterujące 2SA1930 / 2SC5171

Zgodnie z wyborem użytkownika schemat roboczy ma T13 = **2SA1930 (PNP)** i T17 = **2SC5171 (NPN)** zamiast MJE15033/MJE15032. Końcówka nadal ma jedną parę 2SA1943/2SC5200 i cel 100 W / 6 Ω.

## Połączenia

| Element | Baza | Kolektor | Emiter |
|---|---|---|---|
| T13, 2SA1930 PNP | BDP, kolektor T12 | OUTI | BU, przez RBU 4,7 Ω do bazy T14 |
| T17, 2SC5171 NPN | BDN, kolektor T16 | OUTI | BL, przez RBL 4,7 Ω do bazy T18 |

To połączenia funkcjonalnych B/C/E. Dostarczona karta 2SC5171 potwierdza dla T17 nóżki 1=B, 2=C, 3=E, według orientacji rysunku producenta. Numeracji T13 nie potwierdzono. PNP jest w górnej gałęzi, NPN w dolnej. Zachowano dotychczasowe rezystory i połączenia modernizacji. Zamiana typu nie potwierdza poprawności kompensacji ani ustawienia prądu spoczynkowego.

## Status danych katalogowych

Po wcześniejszym braku dostępu sieciowego użytkownik dostarczył kartę **2SC5171.PDF** Toshiba z datą 2006-11-10. Potwierdzono dane i pinout NPN: VCEO = 180 V, IC = 2 A, PC = 20 W przy TC = 25°C lub 2 W przy TA = 25°C; nóżki 1=B, 2=C, 3=E. [Pełny odczyt, chłodzenie i SOA T17](2SC5171-ocena.md).

Karta wskazuje 2SA1930 jako partnera komplementarnego, ale nie potwierdza jego parametrów, pinoutu ani SOA. Dane T13 wymagają osobnej karty. Nie zadeklarowano zgodności całego footprintu z MJE15032/MJE15033 ani zatwierdzenia pracy pary przy nagrzaniu.

## Obciążenie wynikające z modelu

Użyto istniejącego modelu quasi-statycznego z jedną parą końcową, RE = 0,22 Ω, RB = 4,7 Ω, RBE = 68 Ω, R19/R22 = 1,2 kΩ i R20/R21 = 100 Ω. W tabelach przyjęto β końcowego = 20, β drivera = 25, β T12/T16 = 70 oraz stałe VBE = 0,65 V. To scenariusz, a nie potwierdzone minimum wzmocnienia 2SA1930/2SC5171 lub końcowych. Karta 2SC5171 gwarantuje hFE od 100 przy 5 V / 0,1 A oraz od 50 przy 5 V / 1 A, TC = 25°C; nie rozszerzono tych gwarancji na cały przebieg. Wartości modelu pozostawiono bez zmian.

Dla aktywnego górnego drivera obliczono:

```text
VE12 = VOUT + R20 × IE12
VB13 = VC12 = VE12 + VCE12
VE13 = VB13 + VBE
IB13 = IC12 − (V+ − VB13) / R19
IC13 = β13 × IB13
P13 = (VE13 − VOUT) × IC13 + VBE × IB13
```

Dolna gałąź jest w tym uproszczeniu symetryczna. Rzeczywiste różnice obu polaryzacji wymagają osobnych charakterystyk. Średnia w tabeli jest wkładem modelowanej aktywnej gałęzi za cały okres; nie zawiera pełnego bilansu prądu spoczynkowego klasy AB.

### Rezystor, przesunięcie fazowe 0°

| Obciążenie / moc przy założonej amplitudzie | Szyny | Maks. IC drivera | Średni wkład strat na driver | Szczyt chwilowych strat |
|---|---|---:|---:|---:|
| 6 Ω / 100 W | ±50 V | 0,273 A | 1,80 W | 4,54 W |
| 6 Ω / 100 W | ±55 V | 0,273 A | 2,25 W | 5,48 W |
| 4 Ω / 150 W, porównawczo | ±50 V | 0,405 A | 2,52 W | 6,48 W |
| 4 Ω / 150 W, porównawczo | ±55 V | 0,405 A | 3,17 W | 7,84 W |

Przy ±55 V i 6 Ω szczyt strat drivera przypada na około 27,75 V pomiędzy emiterem a kolektorem oraz IC ≈ 0,197 A. Maksymalny prąd i maksymalna strata nie występują w tej samej chwili.

### Przykład obciążenia z przesunięciem 60°

Dla szyn ±55 V i tej samej amplitudy wyjściowej 34,64 V:

| Moduł impedancji | Średni wkład strat na driver | Szczyt chwilowych strat | Punkt przy szczycie: VEC / IC |
|---|---:|---:|---|
| 6 Ω | 3,44 W | 12,44 W | 54,80 V / 0,227 A |
| 4 Ω, porównawczo | 4,94 W | 18,07 W | 54,09 V / 0,334 A |

Wartości te określają wymagania do porównania z gorącym SOA i modelem cieplnym. Dostarczona karta NPN pozwala już wykonać [porównanie z DC SOA 2SC5171](2SC5171-ocena.md): dla przykładu 6 Ω / 60° są wyjścia poza granicę DC. Nie oznacza to automatycznie uszkodzenia przy sygnale audio, ale wykresy pojedynczych impulsów nie zatwierdzają pracy powtarzalnej. Chwilowej mocy nie należy utożsamiać z mocą średnią ani z katalogowym limitem PC przy określonej temperaturze obudowy. Nie sprawdzono również stanów odcięcia i rozruchu.

## Wniosek roboczy

Para została wpisana do schematu zgodnie z wyborem użytkownika. Potwierdzono dane katalogowe i pinout NPN 2SC5171; nie zatwierdzono jeszcze kompletnej pary jako zweryfikowanego zamiennika. Wynik dla 100 W / 6 Ω wymaga zaplanowania chłodzenia sterujących, a następnie sprawdzenia gorącego SOA, temperatur, rzeczywistego wzmocnienia i kompensacji. Praca na kolumnach 4 Ω nadal pozostaje do potwierdzenia.

Kod: [sprawdz_T12_T16.py](sprawdz_T12_T16.py). Wyniki 108 scenariuszy: [T12-T16-wyniki.csv](T12-T16-wyniki.csv), kolumny `driver_*`. Bilans prądów, napięć i mocy sprawdzono dla uproszczonej aktywnej gałęzi; zgodność bilansu nie zastępuje charakterystyk producenta ani symulacji i pomiarów całego wzmacniacza.
