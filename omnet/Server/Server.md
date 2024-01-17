## Parte 1
Il carico in ingresso è λ = 6 richieste al secondo. Il processing rate dei veri sever
è come segue:
- scheda di rete *μn* = 20 richieste al secondo.
- processore *μc* = 10 richieste al secondo.
- disco fisso *μd* = 15 richieste al secondo.

Identificare il tempo di risposta complessivo e le utilizzazioni dei componenti.
Indicare anche l’intervallo di confidenza del 67% per tali valori.

Il tempo di risposta può essere calcolato come:

$$\frac{1}{\mu _n - \lambda}+\frac{1}{\mu _c - \lambda}+\frac{1}{\mu _d - \lambda} \approx 0,412$$

Effettuando la simulazione, avremo questi dati:
```
#	ResponseTime	sigma(ResponseTime)	Utilization_net	sigma(Utilization_net)	Utilization_cpu	sigma(Utilization_cpu)	Utilization_disk	sigma(Utilization_disk)
0.434831258407182	0.0016207369101978305	0.301636952677224	0.0014278612637812686	0.601819184880976	0.0012009208133370011	0.40068597571043396	0.000872775272235666
```

E' possibile notare un tempo di risposta medio di circa 0,4348, simile a quanto dedotto su carta dalla precedente equazione.

Per quanto concerne l'intervallo di confidenza:

$\mu \pm \sigma -> 67 \%$

Quindi:

1) **RETE:** $0.301636952677224 \pm 0.0014278612637812686 -> 67 \%$
2) **CPU:** $0.601819184880976 \pm 0.0012009208133370011 -> 67 \%$
3) **DISCO:** $0.40068597571043396 \pm 0.000872775272235666 -> 67 \%$


## Parte 2

Qual è il compomente collo di bottiglia? E' la CPU in quanto ha un processing rate (tasso di partenza) inferiore rispetto agli altri due nodi. 

Per calcolare il valore massimo di λ al fine di avere un tempo di risposta minore di 0,7 secondi:

$$\frac{1}{\mu _n - \lambda}+\frac{1}{\mu _c - \lambda}+\frac{1}{\mu _d - \lambda} < 0,7$$

Risolvendo la disequazione, avremo circa 8,11.

Volendolo validare mediante simulazione, si noterà che il valore di λ dovrà essere al più 7,9 circa (*vedere file server.data.txt per i dati completi*).

## Parte 3

Viene ricalcolato il valore massimo di λ (considerando che nel caso della CPU λ viene dimezzata):
$$\frac{1}{\mu _n - \lambda}+\frac{1}{\mu _c - \lambda/2}+\frac{1}{\mu _d - \lambda} < 0,7$$

Risolvendo la disequazione, avremo circa 12,3 (un valore circa raddoppiato).

Simulando, ed ovviamente applicando un oggetto router che bilanci le richieste tra i due valori con una politica *Round Robin*, il valore minimo di λ sarà all'incirca pari a 12,2, simile a quanto si è potuto notare dal punto di vista teorico. Avremo un nuovo collo di bottiglia, ovvero il disco.