# Uzgodniony wariant: 100 W / 6 Ω na kanał

## Założenia

- Moc docelowa: 100 W sinusoidalnie na nominalnym obciążeniu 6 Ω.
- Zachować możliwość projektowania do kolumn 4 Ω; moc ciągła na tym obciążeniu pozostaje do ustalenia.
- Dwa transformatory około 250 VA, po jednym na kanał, każdy 2 × 36 V AC bez obciążenia.
- Szyny główne około ±50 V bez obciążenia, sprawdzenie pracy również przy około ±55 V.
- Docelowe stabilizowane szyny VP/VM: wstępnie ±40 V, do sprawdzenia zapasu regulacji.
- Para wejściowa T1/T2: dobrane 2SC2240.
- Posiadane 2SA949 i 2SC2229 są kandydatami odpowiednio na T8 i T9. Nie zatwierdzono jeszcze ich kart producenta ani zamiany wszystkich pozostałych tranzystorów.
- Dwie pary końcowe 2SA1943/2SC5200 na kanał, indywidualne rezystory emiterowe 0,22 Ω.

## Podział zasilania

Stabilizowane VP/VM mają zasilać T1–T10, w miejscu dotychczasowych filtrowanych szyn za R15/R16.

Na głównych szynach zostają T11–T18 wraz z R19/R22. Kolektory T12/T16 są jednocześnie węzłami baz T13/T17 i nie stanowią niezależnych wejść zasilania.

Regulatory muszą być dobrane również do pełnego napięcia wejściowego podczas rozruchu i do zaniku jednej szyny. Budżet obciążenia wyjścia każdego regulatora: wstępnie do 20 mA na kanał. Dla 55 V na wejściu i 40 V na wyjściu odpowiada to około 0,30 W strat tranzystora szeregowego, bez strat układu odniesienia.

Przy obniżeniu VP/VM do ±40 V rezystory R7/R12 trzeba ponownie dobrać. Wartości około 20–20,5 kΩ są punktem wyjścia do zachowania zbliżonych prądów; nie stanowią jeszcze zatwierdzonej listy elementów. Poprzednich 25,5 kΩ nie należy automatycznie przenosić do nowego wariantu.

## Wymagany sygnał wyjściowy

Dla 100 W na 6 Ω:

- napięcie skuteczne: sqrt(100 × 6) = 24,49 Vrms;
- amplituda napięcia: 34,64 V;
- prąd skuteczny: 4,08 A;
- amplituda prądu: 5,77 A.

Przy tym samym napięciu na 4 Ω moc wyniosłaby 150 W, a prąd szczytowy 8,66 A. To wynik obliczenia, nie deklaracja osiągniętej mocy ciągłej. Trzeba sprawdzić spadek napięcia zasilacza, chłodzenie, SOA i zabezpieczenie.

Przy zachowaniu poprzedniego wzmocnienia około 24,5 V/V napięcie wejściowe dla 100 W/6 Ω wyniosłoby około 1,00 Vrms.

## Budżet mocy i zapas napięcia

Dla idealizowanego stopnia klasy B i stałych szyn ±50 V, przy 100 W/6 Ω pobór DC wynosi około 183,8 W, a straty stopnia około 83,8 W. Dochodzą prąd spoczynkowy, sterowanie, rezystory i straty zasilacza. Moc znamionowa transformatora w VA nie jest równa dostępnej mocy DC przy prostowniku z filtrem pojemnościowym.

Przy hipotetycznych 150 W/4 Ω i tej samej amplitudzie pobór DC wynosi około 275,7 W, jeszcze bez pozostałych strat. Nie należy obiecywać takiej mocy ciągłej z transformatora 250 VA.

Stabilizowane ±40 V są punktem wyjścia. Kaskoda, wtórniki i rezystory R20/R21 zabierają część zakresu napięciowego. Wymagane 34,64 V amplitudy trzeba potwierdzić dla temperatury, rozrzutu VBE/hFE i obu polaryzacji sygnału. Również główne szyny muszą utrzymać wymagany zapas pod obciążeniem.

Jeżeli doliny tętnień głównego zasilania spadną poniżej napięcia wymaganego przez regulator, stabilizacja zostanie utracona. Ustawienie ±40 V wymaga sprawdzenia przy obciążeniu i niskim napięciu sieci.

## Aktualny stan

To zapis celu projektu i obliczeń wstępnych. Schemat PDF/PNG/SVG nadal wymaga aktualizacji do stabilizatorów i nowego doboru elementów. Nie wykonano symulacji z modelami producentów ani pomiarów. Układ polaryzacji, kompensacja, limiter SOA, ochrona głośnika przed DC i ochrona termiczna pozostają do opracowania.
