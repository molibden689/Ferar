# 2SC5171 na T17 — odczyt dostarczonej karty

Źródło: przesłany przez użytkownika plik `2SC5171.PDF`, karta Toshiba z datą 2006-11-10, strony 1–3. Odczytano tabelę parametrów, rysunek obudowy oraz wykres SOA. Dane tej karty dotyczą NPN 2SC5171; wskazanie 2SA1930 jako partnera komplementarnego nie potwierdza parametrów ani pinoutu PNP.

## Potwierdzone parametry

| Parametr | Wartość i warunki |
|---|---|
| VCBO / VCEO | 180 V / 180 V |
| VEBO | 5 V |
| IC / IB | 2 A / 1 A |
| PC | 20 W przy TC = 25°C; 2 W przy TA = 25°C |
| Tj max | 150°C |
| hFE(1) | 100–320 przy VCE = 5 V, IC = 0,1 A, TC = 25°C |
| hFE(2) | minimum 50 przy VCE = 5 V, IC = 1 A, TC = 25°C |
| VCE(sat) | typ. 0,16 V, maks. 1 V przy IC = 1 A, IB = 0,1 A |
| VBE | typ. 0,68 V, maks. 1,5 V przy VCE = 5 V, IC = 1 A |
| fT | typ. 200 MHz przy VCE = 5 V, IC = 0,3 A |
| Cob | typ. 16 pF przy VCB = 10 V, IE = 0, f = 1 MHz |
| Obudowa | Toshiba 2-10R1A, raster 2,54 ± 0,25 mm |
| Wyprowadzenia | **1 = B, 2 = C, 3 = E**, w orientacji rysunku producenta |

Gwarancje hFE dotyczą podanych punktów pomiaru; nie wolno rozszerzać minimum 100 na dowolny prąd i temperaturę. fT i Cob są wartościami typowymi, nie dodatkowymi gwarantowanymi minimami lub maksimami. Karta nie deklaruje jawnie elektrycznego potencjału powierzchni radiatorowej; nie wyprowadzono go z samego oznaczenia nóżki 2.

## Fizyczne wyprowadzenia T17 w tym schemacie

| Nóżka 2SC5171 | Funkcja | Sieć projektu |
|---|---|---|
| 1 | baza | BDN, kolektor T16 i połączenie R22 od strony T16 |
| 2 | kolektor | OUTI |
| 3 | emiter | BL, przez RBL = 4,7 Ω do bazy T18 |

To pozwala ustalić przypisanie padów T17, ale nie oznacza, że zaprojektowano lub sprawdzono już footprint PCB. Numeracji 2SA1930 nie potwierdzono tą kartą.

## Chłodzenie

Z wartości PC i Tj można wyliczyć nominalne granice cieplne:

```text
RθJC ≈ (150 − 25) / 20 = 6,25 K/W
RθJA ≈ (150 − 25) / 2 = 62,5 K/W
```

To wyniki obliczenia z podanych mocy, nie osobne parametry Rθ przepisane z tabeli. Nie ma charakterystyki przejściowej Zθ(t). Przy liniowym obniżaniu limitu cieplnego PC(TC) = 20 × (150 − TC) / 125: dla TC = 70°C otrzymujemy 12,8 W. Ten limit cieplny nie zastępuje ograniczenia wtórnego przebicia widocznego w SOA.

W [obecnym modelu](T13-T17-ocena.md), dla 100 W / 6 Ω, β końcowego = 20 i β drivera = 25 średni wkład strat T17 wynosi około 1,80 W przy ±50 V albo 2,25 W przy ±55 V. Do pełnego bilansu klasy AB dochodzi niezamodelowany dokładnie udział spoczynkowy. Limit 2 W przy TA = 25°C nie daje tu odpowiedniego zapasu; trzeba przewidzieć chłodzenie i sprawdzić temperaturę obudowy.

## SOA — odczyt i porównanie

Wykres na stronie 3 podaje DC dla **TC = 25°C**. Orientacyjny odczyt krzywej DC:

| VCE | Dopuszczalny IC przy TC = 25°C, odczyt przybliżony |
|---|---:|
| 30 V | około 0,30 A |
| 50 V | około 0,11 A |
| 55 V | około 0,09 A |
| 100 V | około 0,022 A |

Nie jest to tabela gwarantowanych punktów producenta ani dokładna interpolacja. Widać jednak, że dopuszczalny prąd przy wysokim napięciu jest znacznie mniejszy niż 20 W / VCE.

Producent wymaga liniowego obniżania krzywych wraz z temperaturą. Dla kontroli przy TC = 70°C przyjęto współczynnik (150 − 70) / (150 − 25) = 0,64. Wtedy punkt 50 V daje orientacyjnie około 70 mA DC, a nie 0,11 A. Sam wykres nie podaje osobnego równania deratingu ani modelu impulsów powtarzalnych.

Dla rezystora 6 Ω, szyn ±55 V i przyjętych β = 20/25 model daje między innymi:

- około 0,181 A przy VCE ≈ 30 V;
- około 0,110 A przy VCE ≈ 40 V;
- około 0,039 A przy VCE ≈ 50 V.

Przebieg mieści się z zapasem względem krzywej DC przy TC = 25°C w analizowanym zakresie, ale nie uznano tego za potwierdzenie pracy na gorąco. Przy TC = 70°C porównanie w okolicy 35–40 V staje się graniczne; dokładny margines wymaga lepszego odczytu SOA i potwierdzenia rzeczywistych prądów, temperatur oraz charakterystyk tranzystorów.

Dla przykładowego przesunięcia fazowego 60°, 6 Ω i ±55 V model daje około **0,245 A przy 50 V**, wobec orientacyjnej granicy DC około 0,11 A już przy TC = 25°C. To wyjście poza konserwatywną granicę DC, a nie dowód uszkodzenia przy sygnale audio. Krzywe 100 μs, 1 ms, 10 ms i 100 ms w karcie dotyczą wyłącznie **pojedynczego niepowtarzalnego impulsu**. Nie potwierdzają automatycznie okresowego obciążenia kolumną; potrzebna jest kontrola czasu impulsów, SOA i temperatur w pracy powtarzalnej.

## Wniosek

2SC5171 jest według producenta przeznaczony do stopni sterujących i pozostaje uzasadnionym kandydatem na T17 dla celu 100 W / 6 Ω. Potwierdzono jego dane katalogowe i numerację B/C/E. Nie zatwierdzono jeszcze całej trajektorii przy nagrzaniu ani pracy na rzeczywistej kolumnie 4 Ω. Wymagane są chłodzenie i kontrola kompensacji. Karta 2SA1930 pozostaje osobnym źródłem do sprawdzenia T13.
