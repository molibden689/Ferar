# Uzgodniony wariant: 100 W / 6 Ω na kanał

**Po ponownej kontroli oryginału:** poprawiono R12 na GND–IB2 i wycofano obliczenia z jego błędnego połączenia VB8–IB2. R13 i dobór diod wymagają wyjaśnienia. [Raport porównania i aktualne połączenia](porownanie-z-oryginalem.md).

## Założenia

- Moc docelowa: 100 W sinusoidalnie na nominalnym obciążeniu 6 Ω.
- Wcześniejszy postulat pracy także na kolumnach 4 Ω pozostaje do sprawdzenia dla jednej pary. Moc ciągła i dopuszczalne obciążenie reaktywne na 4 Ω nie zostały zatwierdzone.
- Dwa transformatory około 250 VA, po jednym na kanał, każdy 2 × 36 V AC bez obciążenia.
- Szyny główne około ±50 V bez obciążenia, sprawdzenie pracy również przy około ±55 V.
- Docelowe stabilizowane szyny VP/VM: wstępnie ±40 V, do sprawdzenia zapasu regulacji.
- Para wejściowa T1/T2: dobrane 2SC2240.
- T8: 2SA949 i T9: 2SC2229, dobrane na podstawie dostarczonych kart Toshiba i wstępnej kontroli DC SOA. [Dane i ocena T8](2SA949-ocena.md), [dane i ocena T9](2SC2229-ocena.md). Nie zatwierdzono automatycznej zamiany wszystkich pozostałych tranzystorów na tę parę.
- Jedna para końcowa na kanał, zgodnie z decyzją użytkownika: T14 = 2SA1943 (górny PNP), T18 = 2SC5200 (dolny NPN).
- Sterujące wybrane przez użytkownika: T13 = 2SA1930 (PNP), T17 = 2SC5171 (NPN). Osobne dostarczone karty potwierdzają dane oraz pinout [PNP](2SA1930-ocena.md) i [NPN](2SC5171-ocena.md): oba 1=B, 2=C, 3=E. Dopuszczalna praca pary na gorąco pozostaje do potwierdzenia. [Ocena obciążenia](T13-T17-ocena.md).
- Po jednym rezystorze emiterowym 0,22 Ω / 5 W (RE1/RE2), bazowym 4,7 Ω (RBU/RBL) i baza–emiter 68 Ω (R24/R23) na tranzystor końcowy. Topologia lokalnego sprzężenia pozostaje taka jak w dotychczasowym wariancie modernizacji.

## Podział zasilania

Stabilizowane VP/VM mają zasilać T1–T10 oraz kolektory T11/T15. Na rysunku są osobnymi wejściami zewnętrznego zasilania; nie są połączone z głównymi szynami przez R15/R16.

Główny stopień wyjściowy T12–T18 wraz z R19/R22 zachowuje połączenia z głównymi szynami. Kolektory T12/T16 są jednocześnie węzłami baz T13/T17 i nie stanowią niezależnych wejść zasilania.

Regulatory muszą być dobrane również do pełnego napięcia wejściowego podczas rozruchu i do zaniku jednej szyny. Budżet obciążenia wyjścia każdego regulatora: wstępnie do 30 mA na kanał. Dla 55 V na wejściu i 40 V na wyjściu odpowiada to około 0,45 W strat tranzystora szeregowego, bez strat układu odniesienia.

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

Przy jednej parze idealizowane średnie straty przypadające na jeden tranzystor wynoszą około 41,9 W przy ±50 V i 51,1 W przy ±55 V. To średnia za pełny okres, przed wydzieleniem strat na rezystorach i uwzględnieniem udziału sterujących; nie jest to porównanie chwilowego punktu pracy z SOA. Dla rezystora 6 Ω i RE = 0,22 Ω około 1,83 W na każdą połówkę przejmuje rezystor emiterowy, pomijając prądy baz. Zmniejszenie liczby par nie zmniejsza w podobnej proporcji całkowitego ciepła oddawanego do radiatora.

Jedna para oznacza około 5,77 A szczytowo przez aktywny tranzystor przy 100 W / 6 Ω, bez podziału prądu na dwa równoległe elementy. Trzeba osobno zweryfikować jego gorące SOA, wysterowanie 2SA1930/2SC5171, warunki chłodzenia i ograniczenie przeciążenia.

Przy hipotetycznych 150 W/4 Ω i tej samej amplitudzie pobór DC wynosi około 275,7 W, jeszcze bez pozostałych strat. Nie należy obiecywać takiej mocy ciągłej z transformatora 250 VA.

W tym porównawczym scenariuszu jedna para miałaby idealizowane straty około 62,8 W na tranzystor przy ±50 V lub 76,6 W przy ±55 V, przed wydzieleniem strat w rezystorach. Obliczenie dla rezystora nie potwierdza odporności na rzeczywistą kolumnę 4 Ω.

Stabilizowane ±40 V są punktem wyjścia. Kaskoda, wtórniki i rezystory R20/R21 zabierają część zakresu napięciowego. Wymagane 34,64 V amplitudy trzeba potwierdzić dla temperatury, rozrzutu VBE/hFE i obu polaryzacji sygnału. Również główne szyny muszą utrzymać wymagany zapas pod obciążeniem.

Jeżeli doliny tętnień głównego zasilania spadną poniżej napięcia wymaganego przez regulator, stabilizacja zostanie utracona. Ustawienie ±40 V wymaga sprawdzenia przy obciążeniu i niskim napięciu sieci.

## Aktualny stan

To zapis celu projektu i obliczeń wstępnych. Schemat PDF/PNG/SVG pokazuje już osobne wejścia VP/VM oraz roboczy dobór tranzystorów. Sam układ stabilizatorów pozostaje do opracowania. Nie wykonano symulacji z modelami producentów ani pomiarów. Układ polaryzacji, niepewna wartość R13, kompensacja, limiter SOA, ochrona głośnika przed DC i ochrona termiczna pozostają do opracowania.
