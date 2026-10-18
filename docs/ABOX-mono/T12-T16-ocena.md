# T12 / T16 — ocena 2SC2229 / 2SA949

**Zakres po ponownej kontroli oryginału:** model dotyczy zmodyfikowanego stopnia z rezystorami emiterowymi końcowych i sprzężeniem do OUTI, a nie oryginalnego stopnia z kolektorowymi R28/R29. Nie potwierdza on polaryzacji kaskody; wykryty błąd R12 oraz niepewność R13 opisano w [raporcie porównania](porownanie-z-oryginalem.md).

**Aktualizacja do jednej pary końcowej:** wszystkie poniższe wyniki oraz CSV przeliczono dla jednego T14 = 2SA1943 i jednego T18 = 2SC5200. Wiersze 4 Ω są porównawcze i nie zatwierdzają pracy wzmacniacza na takim obciążeniu.

## Wynik

Para jest możliwym doborem roboczym dla celu 100 W / 6 Ω. Obliczona trajektoria na obciążeniu rezystancyjnym mieści się w gorącym DC SOA obu kart przy przyjętych parametrach tranzystorów. Nie ma podstaw do odrzucenia jej tylko z powodu obudowy TO-92MOD.

Nie potwierdzono jeszcze odporności na rzeczywistą kolumnę 4 Ω we wszystkich temperaturach, przebiegach i stanach przeciążenia. Schemat pokazuje obecnie tę parę jako dobór roboczy T12/T16; niniejsza ocena nie zatwierdza automatycznie całego wzmacniacza ani jego zabezpieczenia.

## Zakres obliczeń

- T12: rozważany 2SC2229 NPN; T16: rozważany 2SA949 PNP.
- Główne szyny ±50 V oraz kontrolnie ±55 V.
- Wariant z kolektorami buforów T11/T15 zasilanymi ze stabilizowanych ±40 V.
- Amplituda wyjścia 34,641 V, odpowiadająca 100 W na 6 Ω. Przy tej samej amplitudzie rezystor 4 Ω pobrałby 150 W. Osiągnięcie amplitudy wymaga osobnej kontroli zapasu kaskody i zasilacza.
- Jedna para końcowa, po jednym RE = 0,22 Ω, RB = 4,7 Ω i RBE = 68 Ω na tranzystor; R19/R22 = 1,2 kΩ, R20/R21 = 100 Ω.
- Przyjęte VBE = 0,65 V, stałe w tym uproszczeniu.
- Scenariusze β końcowych: 20/40/80, β sterujących T13/T17: 25/40/80, β T12/T16 = 70. T13/T17 są obecnie wybrane jako 2SA1930/2SC5171. Wartości β pozostają założeniami obliczeniowymi, nie gwarantowanymi minimami w całym zakresie temperatury, prądu i napięcia. Osobne dostarczone karty PNP i NPN podają hFE od 100 przy |VCE| = 5 V / |IC| = 0,1 A i od 50 przy 5 V / 1 A, TC = 25°C; nie przeniesiono tych gwarancji na cały przebieg. Karty 2SC2229/2SA949 podają hFE od 70 przy 5 V i 10 mA; nie gwarantują tej wartości wszędzie.

Model uwzględnia prądy baz końcowych i driverów, prądy rezystorów baza–emiter, spadki na rezystorach bazowych i emiterowych oraz prąd R19/R22. Uwzględnia też udział prądów drivera i T12/T16 w prądzie wyjściowym.

Usunięto mnożniki wynikające z dwóch równoległych tranzystorów. Suma dwóch spadków VBE w ścieżce tranzystor końcowy–driver pozostaje. RE przewodzi prąd emitera końcowego oraz prąd RBE; nie należy utożsamiać całego prądu RE z prądem samego tranzystora.

Nie jest to symulacja SPICE ani pełny model złączy. Nie uwzględnia pojemności, sprzężenia cieplnego, rozruchu, działania limitera, nasycenia i ustalonego prądu obu gałęzi w obszarze przejścia przez zero. Średnia moc w CSV oznacza wkład modelowanej aktywnej gałęzi; nie stanowi pełnego bilansu cieplnego w klasie AB.

## Obciążenie rezystancyjne

Dla niższych rozpatrywanych β końcowych = 20 i driverów = 25:

| Obciążenie | Maksymalna chwilowa strata przy ±50 V | Przy ±55 V | Maksymalny prąd kolektora T12/T16 |
|---|---:|---:|---:|
| 6 Ω | 0,231 W | 0,277 W | 14,17 mA |
| 4 Ω | 0,314 W | 0,378 W | 20,52 mA |

Szczyt strat przy ±55 V przypada przy napięciu wyjściowym około 22 V, nie przy szczycie sinusoidy. Wysokie napięcie kolektor–emiter przeciwnej, odciętej gałęzi nie występuje jednocześnie z jej maksymalnym prądem.

Wykresy SOA dostarczonych kart dają przy 25°C w tym zakresie napięć granicę DC około 0,8 W. Po wymaganym obniżeniu dla 70°C pozostaje około 0,512 W. Cały policzony aktywny przebieg na rezystorze mieści się w tym ograniczeniu.

## Kolumna z przesunięciem fazowym

Dla ilustracji: sinusoidalny prąd opóźniony o 60° względem napięcia, te same amplitudy, główne ±55 V i β = 20/25:

| Moduł impedancji | Szczyt chwilowych strat | Średni wkład modelowanej aktywnej gałęzi |
|---|---:|---:|
| 6 Ω | 0,635 W | 0,178 W |
| 4 Ω | 0,886 W | 0,243 W |

Taka trajektoria wychodzi chwilowo poza konserwatywną granicę gorącego DC SOA. To nie jest samo w sobie dowodem uszkodzenia: średnia moc jest niższa, a krótkie impulsy mogą być dopuszczalne. Jednak wykresy impulsowe kart dotyczą impulsów pojedynczych, nie gwarantują automatycznie pracy z powtarzalnym sygnałem audio. Częstotliwość, czas trwania impulsów i cieplny przebieg okresowy wymagają osobnej kontroli.

Przy wyższych β = 40/40 dla tego samego przesunięcia 60° szczyty spadają do około 0,300 W na 6 Ω i 0,405 W na 4 Ω. Wynik zależy więc od rzeczywistego wzmocnienia i obciążenia, a nie tylko od nominalnej impedancji kolumny. Każdy tranzystor końcowy przewodzi teraz cały prąd swojej gałęzi, dlatego jego β trzeba oceniać przy większym prądzie niż w wariancie dwóch par.

## Decyzja projektowa

- Dla 100 W / 6 Ω para 2SC2229/2SA949 jest technicznie uzasadnionym kandydatem na T12/T16 do dalszych badań.
- Wcześniejszy postulat pracy na kolumnach 4 Ω wymaga potwierdzenia dynamicznego SOA, temperatur i działania zabezpieczeń przy jednej parze końcowej. Nie uznano 2SC2229/2SA949 za nieodpowiednie wyłącznie na podstawie chwilowej mocy większej od limitu DC.
- Mocniejsze tranzystory w większych obudowach dają większy zapas cieplny, lecz również wymagają kontroli dynamiki i kompensacji.

Kod odtwarzający obliczenia: [sprawdz_T12_T16.py](sprawdz_T12_T16.py). Wyniki scenariuszy: [T12-T16-wyniki.csv](T12-T16-wyniki.csv).

CSV zawiera też prąd, napięcie i straty aktywnego drivera: [interpretacja T13/T17](T13-T17-ocena.md). Zmiana typów na 2SA1930/2SC5171 nie zmienia wyników modelu przy tych samych założonych β i VBE; nie oznacza to potwierdzenia równoważności fizycznych tranzystorów.

Wykonano 108 scenariuszy. Dodatkowa kontrola odtwarza prądy z napięć na elementach i sprawdza bilans prądów, spadków napięcia oraz mocy aktywnej gałęzi, niezależnie od współczynników użytych do wyznaczenia punktu pracy. Maksymalne reszty numeryczne wyniosły około 6,1 × 10⁻¹⁴ A, 5,8 × 10⁻¹⁵ V i 2,1 × 10⁻¹² W. Jest to sprawdzenie spójności uproszczonego modelu; nie waliduje rzeczywistych charakterystyk tranzystorów, polaryzacji ani stabilności układu.
