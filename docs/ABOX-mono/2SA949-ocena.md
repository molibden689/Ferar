# 2SA949 — dane z dostarczonej karty Toshiba

Źródło: plik `2SA949.PDF` przekazany przez użytkownika, cztery strony Toshiba, data dokumentu 2006-11-09. Odczytano tabelę parametrów oraz rysunki wyprowadzeń, DC SOA i zależności mocy od temperatury. Ocena nie opiera się na założeniu identyczności parametrów z 2SC2229.

## Parametry PNP

| Parametr | Wartość i warunki |
|---|---|
| VCEO | −150 V |
| VCBO | −150 V |
| VEBO | −5 V |
| IC, ciągły | −50 mA |
| IB, wartość graniczna | 5 mA |
| PC | 800 mW przy Ta = 25°C |
| Tj maks. | 150°C |
| hFE | 70–240 przy VCE = −5 V, IC = −10 mA |
| Grupa O | hFE 70–140 |
| Grupa Y | hFE 120–240 |
| fT | typowo 120 MHz przy VCE = −30 V, IC = −10 mA |
| Cob | typowo 4 pF, maks. 5 pF przy VCB = −10 V, IE = 0, f = 1 MHz |
| VCE(sat) | maks. moduł 0,8 V przy IC = −10 mA, IB = −1 mA |
| Obudowa | TO-92MOD, Toshiba 2-5J1A |
| Numeracja wyprowadzeń | 1 — emiter, 2 — kolektor, 3 — baza; orientacja według rysunku producenta |

Dla porównania dostarczona karta 2SC2229 podaje VCBO = 200 V, limit IB = 20 mA i VCE(sat) do 0,5 V przy odpowiednich dodatnich prądach. Nie wszystkie parametry pary są więc symetryczne.

## T8 — około 3 mA

Dla stabilizowanych szyn VP/VM około ±40 V przyjęto do kontroli maksymalny moduł VEC około 80 V:

P ≈ 80 V × 0,003 A = 0,24 W.

Wykres pracy ciągłej SOA na stronie 3 dopuszcza przy 80 V około 10 mA przy 25°C. Dopuszczalna moc maleje liniowo od 0,8 W przy 25°C do zera przy 150°C. Przy 70°C:

PC ≈ 0,8 × (150 − 70)/(150 − 25) = 0,512 W.

Przy 80 V odpowiada to około 6,4 mA. Przyjęte 3 mA i 0,24 W mieszczą się we wstępnie odczytanym DC SOA i ograniczeniu cieplnym także przy 70°C. W dotychczasowym schemacie z filtrowanymi szynami bliskimi ±50 V konserwatywne 100 V / 3 mA oznacza około 0,30 W, również poniżej tego limitu.

Rzeczywisty prąd T8 ma też składową dynamiczną: ładuje pojemności kompensacji i steruje następnym stopniem. Powyższe obliczenie nie zatwierdza automatycznie pełnych przebiegów podczas szybkich zmian sygnału, rozruchu, przesterowania ani awarii. Te stany wymagają dalszej weryfikacji.

W projekcie wstępnym przyjęto T8 = 2SA949, obok T9 = 2SC2229.

## Pozostałe pozycje

Sama kontrola punktu 3 mA / 80 V nie zatwierdza wykorzystania tej pary jako wszystkich wtórników i sterujących. Dla T11/T15 oraz T12/T16 trzeba uwzględnić rzeczywisty przebieg prądu, napięcia, temperaturę i SOA.

Schemat nadal nie zawiera docelowych stabilizatorów. Układ polaryzacji, kompensacja i zabezpieczenia całego wzmacniacza pozostają do opracowania.
