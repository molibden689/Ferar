# 2SC2229 — dane z dostarczonej karty Toshiba

Źródło: plik `2SC2229.PDF` przekazany przez użytkownika, trzy strony Toshiba, data dokumentu 1997-09-01. Karta została odczytana wizualnie, łącznie z wykresami SOA i obniżania dopuszczalnej mocy z temperaturą. Nie zakładano parametrów 2SA949 na podstawie tej karty NPN.

## Parametry

| Parametr | Wartość i warunki |
|---|---|
| VCEO | 150 V |
| VCBO | 200 V |
| VEBO | 5 V |
| IC, ciągły | 50 mA |
| PC | 800 mW przy Ta = 25°C |
| Tj maks. | 150°C |
| hFE | 70–240 przy VCE = 5 V, IC = 10 mA |
| Grupa O | hFE 70–140 |
| Grupa Y | hFE 120–240 |
| fT | typowo 120 MHz przy VCE = 30 V, IC = 10 mA |
| Cob | typowo 3,5 pF, maks. 5 pF przy VCB = 10 V, IE = 0, f = 1 MHz |
| Obudowa | TO-92MOD, Toshiba 2-5J1A |
| Numeracja wyprowadzeń | 1 — emiter, 2 — kolektor, 3 — baza; orientacja według rysunku producenta |

Wartości graniczne napięcia, prądu i mocy nie oznaczają możliwości jednoczesnej pracy z każdą z nich. fT jest parametrem tranzystora w podanych warunkach pomiaru, nie pasmem gotowego wzmacniacza.

## T9 — źródło około 3 mA

W wariancie stabilizowanych VP/VM około ±40 V przyjęto do wstępnej oceny VCE do około 80 V:

P ≈ 80 V × 0,003 A = 0,24 W.

Wykres DC SOA na stronie 3 dopuszcza przy 80 V około 10 mA przy 25°C. Wykres PC–Ta obniża limit 0,8 W przy 25°C do zera przy 150°C. Przy 70°C dopuszczalna moc wynosi około:

PC(70°C) ≈ 0,8 × (150 − 70)/(150 − 25) = 0,512 W.

Daje to przy 80 V limit około 6,4 mA. Obliczony punkt 3 mA / 80 V mieści się w tych ograniczeniach. To kontrola przyjętego punktu pracy ciągłej, a nie potwierdzenie wszystkich przebiegów rozruchu, przesterowania i uszkodzeń.

W dotychczasowym rysunku z filtrowanymi szynami bliskimi ±50 V T9 może mieć około 100 V przy 3 mA, czyli około 0,30 W. Także ten punkt mieści się we wstępnie odczytanym DC SOA i limicie cieplnym przy 70°C. Rysunek nadal nie zawiera stabilizatorów.

Na tej podstawie w projekcie wstępnym zmieniono oznaczenie T9 na 2SC2229.

## Wtórnik T11 i dalsze stopnie

Przy samym prądzie spoczynkowym około 3 mA i VCE około 80 V straty także wyniosłyby około 0,24 W. Wtórnik pobiera jednak dodatkowy prąd podczas sterowania następnym stopniem; trzeba sprawdzić prądy i temperaturę w całym przebiegu.

Przykładowo 80 V × 10 mA = 0,80 W: granica przy 25°C i przekroczenie limitu przy podwyższonej temperaturze. Dlatego nie zatwierdzono automatycznej zamiany T11 ani T12 na podstawie samego punktu spoczynkowego.

T8 wymaga osobnej weryfikacji dokumentacji PNP 2SA949. Kompensacja i działanie całego wzmacniacza nadal wymagają symulacji i pomiarów.
