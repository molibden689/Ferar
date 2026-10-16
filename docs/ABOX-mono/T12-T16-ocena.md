# T12 / T16 — ocena 2SC2229 / 2SA949

## Wynik

Para jest możliwym doborem roboczym dla celu 100 W / 6 Ω. Obliczona trajektoria na obciążeniu rezystancyjnym mieści się w gorącym DC SOA obu kart przy przyjętych parametrach tranzystorów. Nie ma podstaw do odrzucenia jej tylko z powodu obudowy TO-92MOD.

Nie potwierdzono jeszcze odporności na rzeczywistą kolumnę 4 Ω we wszystkich temperaturach, przebiegach i stanach przeciążenia. Schemat nadal pokazuje wcześniejsze KSC3503/KSA1381 na T12/T16; niniejsza ocena nie zatwierdza automatycznie całego wzmacniacza ani jego zabezpieczenia.

## Zakres obliczeń

- T12: rozważany 2SC2229 NPN; T16: rozważany 2SA949 PNP.
- Główne szyny ±50 V oraz kontrolnie ±55 V.
- Wariant z kolektorami buforów T11/T15 zasilanymi ze stabilizowanych ±40 V.
- Amplituda wyjścia 34,641 V, odpowiadająca 100 W na 6 Ω. Przy tej samej amplitudzie rezystor 4 Ω pobrałby 150 W. Osiągnięcie amplitudy wymaga osobnej kontroli zapasu kaskody i zasilacza.
- Dwie pary końcowe, osobne RE = 0,22 Ω, RB = 4,7 Ω i RBE = 68 Ω; R19/R22 = 1,2 kΩ, R20/R21 = 100 Ω.
- Przyjęte VBE = 0,65 V, stałe w tym uproszczeniu.
- Scenariusze β końcowych: 20/40/80, β MJE15032/MJE15033: 25/40/80, β T12/T16 = 70. Są to założenia obliczeniowe, nie gwarantowane minima w całym zakresie temperatury, prądu i napięcia. Karty 2SC2229/2SA949 podają hFE od 70 przy 5 V i 10 mA; nie gwarantują tej wartości wszędzie.

Model uwzględnia prądy baz końcowych i driverów, prądy rezystorów baza–emiter, spadki na rezystorach bazowych i emiterowych oraz prąd R19/R22. Uwzględnia też udział prądów drivera i T12/T16 w prądzie wyjściowym.

Nie jest to symulacja SPICE ani pełny model złączy. Nie uwzględnia pojemności, sprzężenia cieplnego, rozruchu, działania limitera, nasycenia i ustalonego prądu obu gałęzi w obszarze przejścia przez zero. Średnia moc w CSV oznacza wkład modelowanej aktywnej gałęzi; nie stanowi pełnego bilansu cieplnego w klasie AB.

## Obciążenie rezystancyjne

Dla niższych rozpatrywanych β końcowych = 20 i driverów = 25:

| Obciążenie | Maksymalna chwilowa strata przy ±50 V | Przy ±55 V | Maksymalny prąd kolektora T12/T16 |
|---|---:|---:|---:|
| 6 Ω | 0,231 W | 0,276 W | 13,46 mA |
| 4 Ω | 0,313 W | 0,376 W | 19,28 mA |

Szczyt strat przy ±55 V przypada przy napięciu wyjściowym około 22 V, nie przy szczycie sinusoidy. Wysokie napięcie kolektor–emiter przeciwnej, odciętej gałęzi nie występuje jednocześnie z jej maksymalnym prądem.

Wykresy SOA dostarczonych kart dają przy 25°C w tym zakresie napięć granicę DC około 0,8 W. Po wymaganym obniżeniu dla 70°C pozostaje około 0,512 W. Cały policzony aktywny przebieg na rezystorze mieści się w tym ograniczeniu.

## Kolumna z przesunięciem fazowym

Dla ilustracji: sinusoidalny prąd opóźniony o 60° względem napięcia, te same amplitudy, główne ±55 V i β = 20/25:

| Moduł impedancji | Szczyt chwilowych strat | Średni wkład modelowanej aktywnej gałęzi |
|---|---:|---:|
| 6 Ω | 0,619 W | 0,178 W |
| 4 Ω | 0,863 W | 0,242 W |

Taka trajektoria wychodzi chwilowo poza konserwatywną granicę gorącego DC SOA. To nie jest samo w sobie dowodem uszkodzenia: średnia moc jest niższa, a krótkie impulsy mogą być dopuszczalne. Jednak wykresy impulsowe kart dotyczą impulsów pojedynczych, nie gwarantują automatycznie pracy z powtarzalnym sygnałem audio. Częstotliwość, czas trwania impulsów i cieplny przebieg okresowy wymagają osobnej kontroli.

Przy wyższych β = 40/40 dla tego samego przesunięcia 60° szczyty spadają do około 0,282 W na 6 Ω i 0,373 W na 4 Ω. Wynik zależy więc od rzeczywistego wzmocnienia i obciążenia, a nie tylko od nominalnej impedancji kolumny.

## Decyzja projektowa

- Dla 100 W / 6 Ω para 2SC2229/2SA949 jest technicznie uzasadnionym kandydatem na T12/T16 do dalszych badań.
- Dla docelowej pracy na kolumnach 4 Ω trzeba potwierdzić dynamiczne SOA, temperatury i działanie zabezpieczeń. Nie uznano pary za nieodpowiednią wyłącznie na podstawie chwilowej mocy większej od limitu DC.
- Mocniejsze tranzystory w większych obudowach dają większy zapas cieplny, lecz również wymagają kontroli dynamiki i kompensacji.

Kod odtwarzający obliczenia: [sprawdz_T12_T16.py](sprawdz_T12_T16.py). Wyniki scenariuszy: [T12-T16-wyniki.csv](T12-T16-wyniki.csv).
