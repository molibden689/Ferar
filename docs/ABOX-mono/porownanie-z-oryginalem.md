# Ponowna kontrola połączeń z oryginałem

Źródło: dostarczony skan „Wzmacniacz 40 W o małych zniekształceniach”, Urszula Klapczyńska, „Radioelektronik”, rys. 2, drukowana strona 9. Przerysowanie sprawdzano osobno od modernizacji do nowych napięć i tranzystorów.

## Znalezione błędy poprzedniego rysunku

1. **R12 był błędnie podłączony między VB8 i IB2.** W oryginale R13 łączy VB8 z masą, a R12 łączy masę z bazą T9, kolektorem T10 i górnym końcem C8. Pozioma szyna masy na skanie ma wyraźny punkt połączenia pomiędzy R13 i R12. W rysunkach poprawiono R12 na GND–IB2. [Fragment źródłowego skanu](fragment-oryginalu-R12.png).
2. Przewód N1 do bazy T7 przechodził przez środek symbolu R14. Poprowadzono go poza symbolem.
3. Przewód wspólnych emiterów T1/T2 przechodził przez symbol C5. Przesunięto C5 i jego przewód, pozostawiając czytelne skrzyżowanie samych przewodów bez połączenia.
4. Rc był narysowany jako zwykły rezystor. Dodano suwak połączony z dolnym końcem VL, jak w oryginale.
5. Wszystkie D1–D7 opisano jako 1N4148 bez potwierdzenia równoważności. Wycofano ten zapis. W źródle D1–D3 to BAYP95, D6/D7 mają wspólny opis BAP811, D4/D5 pozostają do wyjaśnienia.
6. Rysunek nie odzwierciedlał omawianych stabilizowanych szyn. W wariancie zmodyfikowanym VP/VM są teraz osobnymi wejściami ±40 V, a kolektory T11/T15 połączono z nimi. Schemat samych stabilizatorów nie jest częścią rysunku końcówki.

## Ważne połączenia oryginału

| Element / węzeł | Oryginalne połączenie |
|---|---|
| R12 | GND → IB2 (baza T9, kolektor T10, górny C8) |
| R13 | VB8 → GND |
| R14, C7 | pomiędzy VP i VB8 |
| T4 | B=N2, C=N1, E=MIR |
| T5 | B=C=MIR, emiter przez R6 do Rd |
| T6 | B=MIR, C=N2, emiter przez R5 do Rd |
| Rd | końce do R5/R6, suwak VP |
| C6 | N1 ↔ VH |
| T7 | B=N1, C=emiter T8, E=katoda D3 |
| T8 | B=VB8, C=VH |
| T9/T10 | T9 E=ET9, B=IB2, C=VL; T10 B=ET9, C=IB2, E=VM |
| R17/R18 | szeregowo między emiterami T11 i T15; środek BM pływa |
| T12/R20 | emiter T12 przez R20 do UP, przed R28 |
| T13 | PNP: emiter do bazy T14, kolektor do UP |
| T16/R21 | emiter T16 przez R21 do LOW, przed R29 |
| T17 | NPN: emiter do bazy T18, kolektor do LOW |
| R28/R29 | w kolektorach końcowych: UP/LOW → OUTI |
| T11/T15 | kolektory na głównych szynach oryginału |

## R13 — niepewność źródłowa

Powiększony skan odczytano jako niejednoznaczny zapis 82 kΩ / 8,2 kΩ. Nie uznano przecinka za jednoznacznie potwierdzony.

Z R14 = 820 Ω wartość 82 kΩ ustawiłaby bazę T8 przy około 0,990 × VP, pomijając mały prąd bazy. Przy VP = 30 V daje to około 29,7 V, czyli wymagany emiter T8 około 30,35 V, podczas gdy emiter T7 jest około 29,35 V. Taki punkt nie zapewnia właściwej pracy kaskody PNP. Wartość 8,2 kΩ dawałaby bazę około 27,27 V i jest elektrycznie wiarygodna, ale sama zgodność obliczeń nie dowodzi odczytu oryginalnej wartości.

W odtworzeniu pokazano obie możliwości z pytajnikiem. W modernizacji 8,2 kΩ pozostaje wartością wstępną do potwierdzenia.

## Jawne zmiany modernizacji

Odtworzenie oryginału zachowuje jedną parę końcową, ±30 V, R15/R16 i oddzielne UP/LOW przed R28/R29. Nie należy go utożsamiać z wariantem 100 W.

Wariant modernizowany ma:

- główne ±50 V i osobne zewnętrzne stabilizowane VP/VM ±40 V;
- kolektory T11/T15 na VP/VM, resztę stopnia wyjściowego przy głównych szynach;
- zmienione typy tranzystorów, w tym 2SA949/2SC2229 na T8/T9, T15/T11 i roboczo T16/T12;
- sterujące T13 = 2SA1930 (PNP), T17 = 2SC5171 (NPN), zgodnie z wyborem użytkownika; wymagają potwierdzenia pinoutu, parametrów i SOA;
- jedną parę końcową: T14 = 2SA1943 (PNP), T18 = 2SC5200 (NPN), zgodnie z późniejszą decyzją użytkownika;
- po jednym rezystorze emiterowym 0,22 Ω / 5 W (RE1/RE2) i bazowym 4,7 Ω (RBU/RBL) na tranzystor końcowy;
- brak oryginalnych kolektorowych R28/R29; przez to UP/LOW zostają zastąpione OUTI i do OUTI wracają też R20/R21 oraz kolektory T13/T17;
- osobne rezystory baza–emiter 68 Ω dla końcowych;
- wstępne R7/R12 = 20,5 kΩ przy ±40 V, zamiast oryginalnych 15 kΩ przy ±30 V;
- podniesione napięcia znamionowe kondensatorów przy szynach.

Przeniesienie rezystorów końcowych z kolektorów do emiterów oraz połączeń lokalnego sprzężenia jest istotną zmianą topologii. Nie jest to dosłowna kopia oryginału. Wymaga osobnej kontroli stabilności, podziału prądów i zabezpieczeń.

Wcześniejszy wariant modernizacji miał dwie pary końcowe. Aktualny usuwa dodatkową parę i jej sześć rezystorów; zachowuje pozostałe połączenia modernizacji. Jedna para jest założeniem projektu 100 W / 6 Ω, a nie potwierdzeniem pracy na dowolnej kolumnie 4 Ω.

## Kontrola i granice wniosku

Oryginał: 68 elementów, 156 pinów, 48 sieci. Modernizacja z jedną parą: 68 elementów, 156 pinów, 50 sieci.

Rysownik eksportuje odcinki przewodów, punkty połączeń i końcówki elementów. Niezależny skrypt porównuje ich graf z listą odczytaną ze skanu oraz z jawnymi zmianami modernizacji. Kontrola obejmuje brakujące piny/elementy, przerwy, zwarcia różnych sieci oraz niepodłączone etykiety.

To dowód zgodności wyeksportowanych połączeń z listą, a nie symulacja układu. Nie potwierdza wartości R13, doboru zamienników diod, polaryzacji, stabilności, mocy 100 W, SOA na kolumnach 4 Ω ani działania zabezpieczeń.

Poprzednie obliczenia oparte na R12 pomiędzy VB8 i IB2 są wycofane. W szczególności R12 nie jest obciążony napięciem pomiędzy szynami. Przy około −40 V i wstępnym R12 = 20,5 kΩ jego spadek to około 38,7 V, prąd około 1,89 mA i moc około 0,073 W — nie około 0,35 W. Polaryzację kaskody trzeba przeliczyć z poprawną masą i po ustaleniu R13.
