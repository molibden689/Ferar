# ABOX — kontrola połączeń i wariant roboczy

**Po uwadze użytkownika ponownie porównano połączenia z oryginalnym skanem. Znaleziono i poprawiono błędne podłączenie R12 oraz niejednoznaczne skrzyżowania przewodów z symbolami elementów.** [Raport porównania](porownanie-z-oryginalem.md).

## Odtworzenie oryginału

Oryginalny rys. 2 z artykułu Urszuli Klapczyńskiej „Wzmacniacz 40 W o małych zniekształceniach”, „Radioelektronik”: ±30 V, jedna para końcowa, rezystory R28/R29 w kolektorach.

- [Odtworzenie oryginału — PNG](oryginal.png)
- [Odtworzenie oryginału — PDF](oryginal.pdf)
- [Odtworzenie oryginału — SVG](oryginal.svg)
- [Niezależna lista oryginalnych połączeń](oryginal-polaczenia.json)
- [Oryginalne połączenia tranzystorów](oryginal-tranzystory.csv)

Zachowano połączenia odczytane ze skanu. Niepewną wartość R13 i oznaczenia części diod opisano jawnie. Nie jest to potwierdzenie poprawności wartości źródłowej ani parametrów działającego wzmacniacza.

## Wariant zmodyfikowany

Cel: 100 W / 6 Ω na kanał. Zgodnie z decyzją użytkownika stopień końcowy ma **jedną parę: T14 = 2SA1943 (PNP), T18 = 2SC5200 (NPN)**. Główne szyny około ±50 V; zewnętrzne stabilizowane VP/VM około ±40 V dla T1–T10 i kolektorów T11/T15. Wcześniejszy postulat pracy także na kolumnach 4 Ω pozostaje do weryfikacji dla jednej pary; nie jest potwierdzoną specyfikacją.

- [Wariant roboczy — PNG](schemat.png)
- [Wariant roboczy — PDF](schemat.pdf)
- [Wariant roboczy — SVG](schemat.svg)
- [Lista połączeń wariantu](polaczenia.json)
- [Tabela tranzystorów](tranzystory.csv)
- [Wymagania i obliczenia wstępne](wariant-100W-6ohm.md)

Na schemacie VP/VM są osobnymi zaciskami zasilania, nie są połączone z głównymi szynami przez R15/R16. Nie zaprojektowano jeszcze wykonawczego układu stabilizatorów. Rozmieszczenie rezystorów końcowych i lokalnych pętli stopnia wyjściowego różni się świadomie od oryginału; szczegóły w raporcie porównania.

Każdy tranzystor końcowy ma jeden rezystor emiterowy 0,22 Ω / 5 W (RE1/RE2), bazowy 4,7 Ω (RBU/RBL) i baza–emiter 68 Ω (R24/R23). Usunięto drugą parę wraz z jej rezystorami. Obliczenia T12/T16 również dotyczą już jednej pary.

2SC2240 pozostają parą wejściową. 2SA949/2SC2229 są wpisane jako dobór roboczy na T8/T9, T15/T11 i T16/T12. Nie oznacza to zatwierdzenia dynamicznego SOA i pracy na dowolnej kolumnie 4 Ω.

## Wynik kontroli

Odtworzona grafika oryginału: **68 elementów, 156 pinów, 48 sieci**. Wariant zmodyfikowany z jedną parą: **68 elementów, 156 pinów, 50 sieci**.

Geometrię przewodów, punkty połączeń, końcówki elementów i etykiety porównano z listą oryginału odczytaną niezależnie ze skanu. Lista wariantu powstaje z listy oryginału przez jawne zmiany topologii. Kontrola wykrywa przerwy, zwarcia różnych sieci, brakujące elementy/piny i niepodłączone etykiety. To kontrola grafu połączeń, nie ERC programu CAD, SPICE ani pomiar wzmacniacza.

## Ograniczenia

**Żaden z rysunków nie jest dokumentacją zatwierdzoną do wykonania PCB lub uruchomienia.**

- R13: nieczytelny lub błędny zapis 82 kΩ / 8,2 kΩ; 82 kΩ daje niespójną polaryzację kaskody, ale nie zastąpiono tego rozstrzygnięciem rzekomo potwierdzonym w źródle.
- D6/D7: zachowano oznaczenie BAP811 ze skanu, bez automatycznej zamiany na 1N4148. D4/D5 nie mają w skanie jednoznacznie podanego typu.
- Polaryzacja, kompensacja, zapas amplitudy, SOA i chłodzenie wymagają dalszych obliczeń, symulacji i pomiarów.
- Limiter SOA, ochrona głośnika przed DC i ochrona termiczna pozostają do opracowania. Nie ma PCB ani Gerberów.

Poprzednie obliczenia zależne od błędnego węzła R12, w szczególności prądu R12 i dzielnika polaryzacji kaskody, są wycofane. Dane katalogowe tranzystorów pozostają prawidłowo odczytane: [2SC2229](2SC2229-ocena.md), [2SA949](2SA949-ocena.md). [Ocena T12/T16](T12-T16-ocena.md) jest uproszczonym modelem wyłącznie zmodyfikowanego stopnia wyjściowego, nie potwierdzeniem oryginału ani całego wzmacniacza.

## Odtwarzanie i kontrola

Python 3, matplotlib i numpy:

```sh
python rysuj_schemat.py --oryginal
python rysuj_schemat.py
python -B sprawdz_polaczenia.py oryginal-polaczenia.json oryginal-geometria.json
python -B sprawdz_polaczenia.py
```

Te same nazwy sieci oznaczają połączenie elektryczne. Skrzyżowania bez kropki nie są połączeniami. Pliki SVG są wektorowe; PNG można otworzyć na GitHub, PDF pobrać i powiększać.
