# 2SA1930 na T13 — odczyt dostarczonej karty

Źródło: dostarczony przez użytkownika plik `2SA1930.PDF`, karta Toshiba z datą 2007-06-15, strony 1–4. Odczytano parametry, rysunek obudowy, SOA i charakterystykę przejściową cieplną. Porównanie NPN opiera się osobno na dostarczonej karcie `2SC5171.PDF`, 2006-11-10.

## Potwierdzone parametry PNP

| Parametr | Wartość i warunki |
|---|---|
| VCBO / VCEO | −180 V / −180 V |
| VEBO | −5 V |
| IC / IB | −2 A / −1 A |
| PC | 20 W przy TC = 25°C; 2 W przy TA = 25°C |
| Tj max / Tstg | 150°C / −55…150°C |
| hFE(1) | 100–320 przy VCE = −5 V, IC = −0,1 A, TC = 25°C |
| hFE(2) | minimum 50 przy VCE = −5 V, IC = −1 A, TC = 25°C |
| VCE(sat) | typ. −0,24 V, granica co do modułu 1 V przy IC = −1 A, IB = −0,1 A |
| VBE | typ. −0,68 V, granica co do modułu 1,5 V przy VCE = −5 V, IC = −1 A |
| fT | typ. 200 MHz przy VCE = −10 V, IC = −0,3 A |
| Cob | typ. 26 pF przy VCB = −10 V, IC = 0, f = 1 MHz — warunki zgodnie z tabelą producenta |
| Obudowa | Toshiba 2-10R1A, JEITA SC-67, raster 2,54 ± 0,25 mm |
| Wyprowadzenia | **1 = B, 2 = C, 3 = E**, według orientacji rysunku producenta |

Znak minus wynika z polaryzacji PNP. Gwarancje hFE dotyczą wyłącznie podanych warunków; nie przeniesiono minimum 100 na cały przebieg, temperaturę i napięcie robocze. Nie potwierdzono tą kartą potencjału elektrycznego powierzchni radiatorowej: numer nóżki kolektora nie jest osobną deklaracją połączenia tej powierzchni.

## Wyprowadzenia T13 w schemacie

| Nóżka 2SA1930 | Funkcja | Sieć projektu |
|---|---|---|
| 1 | baza | BDP, kolektor T12 i połączenie R19 od strony T12 |
| 2 | kolektor | OUTI |
| 3 | emiter | BU, przez RBU = 4,7 Ω do bazy T14 |

Potwierdzono numerację obu wybranych sterujących: T13 = 2SA1930, T17 = 2SC5171 mają 1=B, 2=C, 3=E oraz oznaczenie obudowy Toshiba 2-10R1A. To nie jest zatwierdzenie gotowego footprintu ani istniejącej PCB — takich plików projektu nie ma.

## Różnice względem 2SC5171

| Cecha | 2SA1930 PNP | 2SC5171 NPN |
|---|---|---|
| Cob, typowo | 26 pF przy VCB = −10 V, IC = 0, 1 MHz | 16 pF przy VCB = 10 V, IE = 0, 1 MHz |
| fT, typowo | 200 MHz przy −10 V / −0,3 A | 200 MHz przy 5 V / 0,3 A |
| VCE(sat), typowo | moduł 0,24 V przy 1 A, IC/IB = 10 | 0,16 V przy 1 A, IC/IB = 10 |
| Dodatkowy wykres cieplny | rth–tw na stronie 4 | brak w dostarczonej wersji karty NPN |

Obie karty wskazują partnera komplementarnego, lecz nie są to identyczne charakterystyki ze zmienionym znakiem. Różne Cob i warunki pomiaru fT wymagają uwzględnienia przy kontroli kompensacji. Nie zastąpiono ich w modelu pełnymi charakterystykami pojemnościowymi lub częstotliwościowymi.

## Chłodzenie i przejściowa rezystancja cieplna

Z PC i Tj wynikają nominalnie RθJC ≈ 6,25 K/W i RθJA ≈ 62,5 K/W. Są to obliczenia z (150 − 25) / PC, a nie osobne wartości przepisane z tabeli. Z liniowego obniżania limitu cieplnego wynika PC ≈ 12,8 W przy TC = 70°C; ograniczenie wtórnego przebicia może być ostrzejsze.

Na stronie 4 są krzywe rth(tw) dla pojedynczego niepowtarzalnego impulsu, bez radiatora i z idealnym radiatorem. Producent ogranicza ich stosowanie do obszaru ograniczonego cieplnie. Dają podstawę do zbudowania modelu cieplnego, ale same nie zastępują SOA ani obliczenia temperatury dla powtarzalnego przebiegu audio. Nie przeniesiono wykresu PNP automatycznie na NPN.

[Model stopnia](T13-T17-ocena.md) przy β końcowego = 20, β drivera = 25 i celu 100 W / 6 Ω daje dla T13 średni wkład strat około 1,80 W przy ±50 V lub 2,25 W przy ±55 V. Nie obejmuje pełnego bilansu spoczynkowego klasy AB. Przy limicie 2 W dla TA = 25°C potrzebne jest zaplanowane chłodzenie, z pomiarem temperatury obudowy. Nie uznano 20 W za moc dostępną bez radiatora.

## SOA i zakres wniosku

Na stronie 3 krzywa DC jest podana dla TC = 25°C. Orientacyjny odczyt, zapisany jako moduły napięcia i prądu: przy 30 V prąd jest rzędu 0,3 A, przy 50 V około 0,1 A, a przy 100 V około 0,02 A. To przybliżone odczyty wykresu, nie tabela gwarantowanych punktów. SOA jest dużo węższe niż samo PC / |VCE|. Nie zadeklarowano dokładnej zgodności krzywej z NPN.

Wymagane przez producenta liniowe obniżenie krzywych z temperaturą oszacowano przy TC = 70°C współczynnikiem (150 − 70) / (150 − 25) = 0,64. Wtedy orientacyjna granica przy 50 V jest rzędu 0,064 A DC.

W dotychczasowym symetrycznym modelu dla 6 Ω, ±55 V i β = 20/25 prąd drivera przy |VCE| ≈ 30 / 40 / 50 V wynosi około 0,181 / 0,110 / 0,039 A. Jest to uzasadniony punkt wyjścia dla obciążenia rezystancyjnego. Przy TC = 70°C margines względem DC SOA w środkowej części przebiegu jest mały i nie zatwierdzono całej trajektorii na gorąco na podstawie przybliżonego odczytu.

Dla przykładu z przesunięciem fazowym 60° model daje około 0,245 A przy |VCE| = 50 V — powyżej orientacyjnej granicy DC już przy TC = 25°C. Nie jest to automatyczny dowód uszkodzenia przy audio. Krzywe 100 μs, 1 ms, 10 ms i 100 ms dotyczą pojedynczych niepowtarzalnych impulsów; pracy okresowej trzeba poświęcić osobną kontrolę SOA i cieplną. Karta nie zatwierdza w ten sposób pracy całego wzmacniacza na kolumnach 4 Ω.

## Decyzja robocza

Pozostawiono T13 = 2SA1930 oraz T17 = 2SC5171. Dane i numeracja wyprowadzeń obu typów są teraz potwierdzone w osobnych dostarczonych kartach. Nadal wymagają sprawdzenia chłodzenie, gorące i dynamiczne SOA, rzeczywiste wzmocnienie, kompensacja oraz układ polaryzacji. Nie zmieniono założeń β/VBE ani wyników dotychczasowego uproszczonego modelu.
