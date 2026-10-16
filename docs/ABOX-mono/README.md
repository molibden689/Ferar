# ABOX — końcówka mono, projekt wstępny

Schemat mono bez zasilacza, opracowywany na podstawie dostarczonego skanu artykułu Urszuli Klapczyńskiej „Wzmacniacz 40 W o małych zniekształceniach” z „Radioelektronika”.

Założenia modernizacji: zasilanie około ±50 V bez obciążenia, transformatory 2 × 36 V AC, kolumny nominalnie 6 Ω, docelowo możliwość pracy z 4 Ω. Uwzględnienia wymaga wzrost szyn do około ±55 V przy wyższym napięciu sieci. Para wejściowa: dobrane 2SC2240. Dwie pary końcowe na kanał: 2SA1943/2SC5200, z indywidualnymi rezystorami emiterowymi.

**Aktualny uzgodniony cel: 100 W na 6 Ω na kanał, z docelowym stabilizowanym zasilaniem ±40 V stopni T1–T10.** T11–T18 i R19/R22 pozostają na głównych szynach. [Wymagania tego wariantu i obliczenia](wariant-100W-6ohm.md).

Rysunek w tym katalogu nadal przedstawia wcześniejszą wersję z filtrowaniem VP/VM przez R15/R16, a nie gotowe stabilizatory. Wymaga aktualizacji wraz z polaryzacją i doborem elementów. Przyjęcie celu 100 W nie oznacza, że tę moc już potwierdzono.

## Otwieranie schematu

- [Schemat PNG — podgląd](schemat.png)
- [Schemat PDF — do powiększania i pobrania](schemat.pdf)
- [Schemat SVG — wersja wektorowa](schemat.svg)
- [Tabela połączeń tranzystorów](tranzystory.csv)

Na GitHub plik PNG można otworzyć jako obraz. W przypadku braku podglądu PDF pobierz go przez przycisk pobierania pliku.

Rysunek zawiera przewody i kropki połączeń. Skrzyżowania bez kropki nie są połączeniami. Powtarzające się oznaczenia sieci, np. FB, OUTI, EP1 i BU1, oznaczają te same połączenia elektryczne. Odsprzęganie lokalne jest częścią końcówki; główny zasilacz pozostaje poza schematem.

## Stan projektu

**To schemat do przeglądu, a nie zatwierdzona dokumentacja wykonawcza.** Skontrolowano odtworzenie głównych połączeń względem oryginału. Nie wykonano kontroli ERC w programie CAD, symulacji z modelami tranzystorów ani pomiarów prototypu. Nie ma projektu PCB ani Gerberów.

Do weryfikacji pozostają:

- układ polaryzacji D4–D7/Rc i jego zachowanie termiczne;
- kompensacja C6 oraz stabilność przy dwóch parach końcowych i obciążeniu reaktywnym;
- napięcia, prądy, straty mocy i bezpieczny obszar pracy przy najwyższym napięciu zasilania;
- sterowanie i chłodzenie MJE15032/MJE15033; mogą rozpraszać około 1 W już w spoczynku;
- limiter SOA, ochrona głośnika przed DC i zabezpieczenie termiczne — jeszcze niezaprojektowane;
- zgodność wyprowadzeń z kartami konkretnych producentów;
- rozbieżność między R1 = 150 Ω / C1 = 2,2 nF na oryginalnym rysunku a podanym w tekście filtrem 70 kHz.

Cel początkowego prądu spoczynkowego: 20 mA na tranzystor końcowy, czyli 4,4 mV na każdym 0,22 Ω. To cel do sprawdzenia, nie potwierdzenie działania przedstawionego układu polaryzacji.

Wcześniejsze rysunki miały błędy lustra Wilsona i połączeń sterujących. Ten pakiet zawiera poprawiony rysunek. Wcześniejsze obliczenia stopnia sterującego wymagają ponowienia; nie należy na ich podstawie budować wzmacniacza.

## Odtwarzanie rysunku

Wymagane Python 3, matplotlib i numpy. Z katalogu tego pliku:

```sh
python rysuj_schemat.py
```

Skrypt odtwarza trzy pliki `schemat.pdf`, `schemat.png` i `schemat.svg`. Jest źródłem rysunku wektorowego, a nie projektem KiCad ani symulatorem obwodu.
