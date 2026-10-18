# Propozycja: tranzystorowy mnożnik VBE zamiast D4–D7

Cel: zastąpienie łańcucha D4–D7 i jego regulacji Rc układem o regulowanym napięciu VH–VL i dobranej kompensacji temperaturowej. To propozycja do dalszego opracowania; głównego schematu nie zmieniono jeszcze na układ z poniższymi wartościami przykładowymi.

## Zalecany kierunek

Jeden tranzystor NPN jako mnożnik VBE, roboczo Q19 (np. BD139; konkretny producent i fizyczny pinout pozostają do sprawdzenia). Węzły mnożnika:

| Element | Połączenie |
|---|---|
| Q19 | C = VH, E = VL, B = VBIAS_B |
| RCB | VH → VBIAS_B |
| RBE | VBIAS_B → VL; gałąź z regulacją |

Mnożnik jest dwójnikiem pomiędzy VH i VL; nie łączy się go z masą. Dotychczasowe bazy T11/T15 pozostają odpowiednio na VH/VL. D1–D3 pełnią inne funkcje i nie są przedmiotem tej zamiany.

W przybliżeniu:

```text
V(VH) − V(VL) = VBE19 × (1 + RCB/RBE) + RCB × IB19
```

Regulację korzystnie umieścić w gałęzi baza–emiter, z rezystorem stałym ograniczającym zakres. Zwiększenie jej rezystancji obniża napięcie polaryzacji. Przy użyciu trymera jako reostatu należy połączyć suwak z jednym z końców, aby utrata kontaktu suwaka dawała pełną rezystancję ścieżki. To nie zapewnia odporności na wszystkie możliwe uszkodzenia. Początkowe ustawienie: największa rezystancja tej gałęzi, czyli najmniejsze napięcie polaryzacji. Zakres regulacji trzeba dopiero dobrać do obliczonego prądu spoczynkowego i rozrzutu elementów.

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

Dla czujnika o VBE ≈ 0,65 V mnożnik jest rzędu 4,4. Jako przykład oceny można przyjąć RCB = 3,3 kΩ i RBE = 1 kΩ. Przy prądzie całego dwójnika założonym jako 3 mA otrzymujemy około 2,87 V dla β19 = 100 lub 2,83 V dla β19 = 200. Różnica pokazuje, dlaczego trzeba uwzględnić IB19; nie są to zatwierdzone wartości montażowe. Prąd 3 mA również wymaga potwierdzenia w pełnym punkcie pracy VAS.

## Darlington i kompensacja temperatury

Darlington przede wszystkim zmniejsza wpływ prądu bazy dzięki większemu wzmocnieniu. Ma dwa złącza w ścieżce wejściowej i wymaga innego stosunku rezystorów. Nie gwarantuje lepszej kompensacji cieplnej. Przy zadanym napięciu Vbias zarówno pojedyncze, jak i podwójne złącze można skalować dzielnikiem; samo policzenie złączy nie rozstrzyga współczynnika temperaturowego.

Przy kilku miliamperach prądu dwójnika jeden tranzystor jest rozsądnym punktem wyjścia. Dla mnożnika około 4,4 i przykładowego dVBE/dT ≈ −2 mV/K współczynnik wynosi około −8,8 mV/K. Rzeczywisty wynik zależy od prądu, β, temperatur i rezystorów.

W naszym układzie główne cztery spadki VBE należą do **T11, T12, T15 i T16**. Czujnik powinien śledzić ich temperatury oraz pośredni wpływ pozostałych tranzystorów. Temperatura radiatora końcowych może znacznie różnić się od temperatury tych elementów. Sam montaż Q19 na głównym radiatorze nie dowodzi właściwej kompensacji; może powodować zbyt silny spadek prądu spoczynkowego po rozgrzaniu stopnia mocy.

Do zamknięcia tej zmiany potrzebne są: docelowy IC spoczynkowy końcowych, prąd dostępny dla mnożnika, ograniczony zakres regulacji oraz sposób sprzężenia cieplnego. Potem trzeba sprawdzić IQ przy oddzielnym nagrzewaniu płytki, sterujących i końcowych, a także zachowanie dynamiczne i stabilność. Propozycja nie stanowi jeszcze potwierdzenia dobrej kompensacji gotowego wzmacniacza.
