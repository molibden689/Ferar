# Mnożnik VBE w nowym schemacie

Łańcuch D4–D7 i Rc zastąpiono w [nowym schemacie](schemat.png) tranzystorowym mnożnikiem VBE. [Powiększenie układu](mnoznik-VBE.png), [PDF powiększenia](mnoznik-VBE.pdf). To dobór roboczy, wymagający potwierdzenia prądu spoczynkowego i kompensacji cieplnej, nie dokumentacja wykonawcza PCB.

## Zalecany kierunek

Jeden tranzystor NPN jako mnożnik VBE: Q19 = **2SC5171**, którego kartę użytkownik dostarczył. Zastępuje wcześniejszego kandydata BD139. Karta potwierdza 1=B, 2=C, 3=E, ale nie gwarantuje konkretnego β/VBE przy prądzie kilku mA. Węzły mnożnika:

| Element | Połączenie |
|---|---|
| Q19 = 2SC5171 | C/2 = VH, E/3 = VL, B/1 = VBIAS_B |
| R30 = 3,3 kΩ / 1% | VH → VBIAS_B |
| R31 = 820 Ω / 1% | VBIAS_B → VBIAS_P |
| P1 = 1 kΩ, wieloobrotowy | 1 = VBIAS_P, 2 = VL, W zwarte z 2/VL |

Mnożnik jest dwójnikiem pomiędzy VH i VL; nie łączy się go z masą. Dotychczasowe bazy T11/T15 pozostają odpowiednio na VH/VL. D1–D3 pełnią inne funkcje i nie są przedmiotem tej zamiany.

W przybliżeniu:

```text
RBE_mnożnika = R31 + ustawiona rezystancja P1
V(VH) − V(VL) = VBE19 × (1 + R30/RBE_mnożnika) + R30 × IB19
```

Regulacja jest w gałęzi baza–emiter, z rezystorem stałym ograniczającym zakres. Zwiększenie jej rezystancji obniża napięcie polaryzacji. Suwak P1 jest zwarty z końcem od strony VL; przy utracie kontaktu suwaka pozostaje pełna rezystancja ścieżki, o ile końce i przewód zwarcia są sprawne. To nie zapewnia odporności na wszystkie możliwe uszkodzenia. **START: P1 = 1 kΩ**, największa rezystancja gałęzi i najmniejsze Vbias. Nie deklaruje to zerowego prądu dla dowolnego rozrzutu i temperatur.

Dla I = 3 mA, VBE19 = 0,65 V i β19 = 100 zakres wynosi **1,915–3,338 V**. Przykładowe 2,85 V odpowiada P1 ≈ 190 Ω. To wynik obliczenia, nie nastawa uruchomieniowa ani zatwierdzony prąd spoczynkowy. W ilustracyjnych skrajnych założeniach prądu, VBE, β i tolerancji napięcie przy maksymalnym P1 może dojść do około 2,46 V; konieczna jest kontrola rzeczywistego prądu.

## Ile napięcia wymaga nasz układ?

Z aktualnych połączeń wynika:

```text
Vbias = VBE11 + VBE12 + |VBE15| + |VBE16|
        + R20 × IE12 + R21 × |IE16|
```

To ważna cecha tego złożonego stopnia wyjściowego. Napięcia T13/T17 i końcowych również wpływają na prądy, a przez nie na powyższy warunek, ale nie należy po prostu dodawać sześciu VBE jak w kaskadzie zwykłych wtórników.

Ilustracja DC, **nie ustalenie docelowego prądu**: przy IC końcowych = 30 mA, β końcowych = 50, β driverów = 100, β T12/T16 = 70, wszystkich |VBE| = 0,65 V i szynach ±50 V:

- prąd RBE końcowego: 0,65 / 68 ≈ 9,56 mA;
- prąd bazy końcowego: 30 / 50 = 0,60 mA;
- R19: około 1,130 mA; baza drivera: około 0,101 mA;
- IE12 = |IE16| ≈ 1,249 mA;
- Vbias ≈ 4 × 0,65 + 2 × 100 × 0,001249 ≈ **2,85 V**;
- prąd szeregu R17/R18 ≈ 3,52 mA.

Przy tym przykładzie RE = 0,22 Ω przewodzi około 40,16 mA, czyli daje około 8,84 mV. Prąd ten obejmuje emiter końcowego i bocznik 68 Ω; nie jest równy IC końcowego.

Dla czujnika o VBE ≈ 0,65 V mnożnik jest rzędu 4,4. Przy R30 = 3,3 kΩ i efektywnym R31+P1 = 1 kΩ oraz prądzie całego dwójnika założonym jako 3 mA otrzymujemy około 2,87 V dla β19 = 100 lub 2,83 V dla β19 = 200. Różnica pokazuje, dlaczego trzeba uwzględnić IB19. Prąd 3 mA wymaga potwierdzenia w pełnym punkcie pracy VAS.

## Darlington i kompensacja temperatury

Darlington przede wszystkim zmniejsza wpływ prądu bazy dzięki większemu wzmocnieniu. Ma dwa złącza w ścieżce wejściowej i wymaga innego stosunku rezystorów. Nie gwarantuje lepszej kompensacji cieplnej. Przy zadanym napięciu Vbias zarówno pojedyncze, jak i podwójne złącze można skalować dzielnikiem; samo policzenie złączy nie rozstrzyga współczynnika temperaturowego.

Przy kilku miliamperach prądu dwójnika jeden tranzystor jest rozsądnym punktem wyjścia. Dla mnożnika około 4,4 i przykładowego dVBE/dT ≈ −2 mV/K współczynnik wynosi około −8,8 mV/K. Rzeczywisty wynik zależy od prądu, β, temperatur i rezystorów.

W naszym układzie główne cztery spadki VBE należą do **T11, T12, T15 i T16**. Czujnik powinien śledzić ich temperatury oraz pośredni wpływ pozostałych tranzystorów. Temperatura radiatora końcowych może znacznie różnić się od temperatury tych elementów. Sam montaż Q19 na głównym radiatorze nie dowodzi właściwej kompensacji; może powodować zbyt silny spadek prądu spoczynkowego po rozgrzaniu stopnia mocy. Sposób wspólnego sprzężenia cieplnego czujnika z tą czwórką pozostaje do opracowania i pomiaru.

Do zatwierdzenia pozostają: docelowy IC spoczynkowy końcowych, rzeczywisty prąd dostępny dla mnożnika, dopuszczalny zakres regulacji dla wybranych egzemplarzy oraz sposób sprzężenia cieplnego. Trzeba sprawdzić IQ przy oddzielnym nagrzewaniu płytki, sterujących i końcowych, a także zachowanie dynamiczne i stabilność. Nowy rysunek nie stanowi jeszcze potwierdzenia dobrej kompensacji gotowego wzmacniacza.

Obliczenia: [sprawdz_mnoznik_VBE.py](sprawdz_mnoznik_VBE.py), [wyniki JSON](mnoznik-VBE-kontrola.json). [Raport kontroli nowego schematu](kontrola-nowego-schematu.md) opisuje również jawny dobór R13 = 12 kΩ i ograniczenia amplitudy.
