### AVVIO DI OMNET (test per vedere se va tutto bene)
```bash
cd omnetpp[version]/
. setenv
omnetpp
```

### CARTELLE DI LAVORO

`omnetpp[versione]/samples/queuenet`

Andremo a lavorare con i file Source.ned, Sink.ned, Queue.ned che ci fanno capire come possiamo configurare il source, il sink
ed il server tipo coda.
Nei file .ned di questi tre tipi infatti si possono trovare i vari parametri accettati che si possono passare!

Definiano un modello, per esempio un MM1

andiamo nella cartella

`.../samples/queuenet/`

e creiamo i file sample_MM1.ned e sample_MM1.ini

i modelli che useremo (Source, Sink, Queue) si trovano in .../samples/queueinglib/*

------------

**FILE .ned di configurazione (esempio sample_MM1.ned) - METRICHE**

Nel file di esempio troviamo gli import dei moduli Source, Sink e Queue.
Poi si settano le connessioni tra i vari moduli ed altri parametri.
I vari parametri possono avere valori di default e qui si può dichiarare una grandezza tramite variabile aleatoria che segue determinati andamenti (gaussiana, poisson, log etc...).

**FILE .ini di configurazione (esempio sample_MM1.ini) - SCENARIO**

Nel file sample_MM1.ini invece c'è il setup della simulazione con vari valori numerici e varie impostazioni sulla raccolta dati.
In particolare si possono creare varie simulazioni con vari parametri. 
Ogni simulazione ha un nome tra parentesi quadre (esempio -> [NOME SIM 1]).

*Per fare vari run e non dover scrivere tante righe, si fa uso del linguaggio di templating mako.*

------------

### TEMPLATE MAKO

Se bisogna fare tanti run con varie configurazioni, si usa un template ed uno script python che creeranno un unico file .ini con le specifiche di tutti i run richiesti con i diversi parametri.

Useremo un file di template, ad esempio, sample_MM1.ini.mako che modificheremo (uguale al sample_MM1.ned ma con i vari cicli for e/o le condizioni scritte con il linguaggio di templating, simile a quello usato in Django).
Una volta finito di editare il file .ini.mako, per fare l'update del template usiamo lo script di utility update_template.py

Il file template si troverà nella stessa cartella del file .ini che vorremo creare, ovvero in .../samples/queuenet/
Lo script update_template.py andrà a cercare l'estensione .mako nei file .ini e creerà un'opportuno file senza l'estensione .mako che avrà tutti i dati.

Nel nostro esempio quindi avremo un file sample_MM1.ini.mako che verrà trasformato in sample_MM1.ini

------------

### SIMULAZIONE
A) **RUN DELLA SIMULAZIONE**

Per fare il run della simulazione ho due alternative:

1) uso interfaccia grafica se devo fare poche simulazioni (ne faccio una volta con l'interfaccia grafica - bello ma lungo...);
2) uso makefile per simulazioni multiple ed in parallelo se devo fare più simulazioni con vari parametri diversi (non vedo nulla ma fa tutto lui).

Quindi:
1) USO INTERFACCIA GRAFICA

Dentro la cartella omnetpp[version]/samples/queuenet eseguo il comando:

`./queuenet [filesimulazione].ini`

*Il comando queuenet lancia il file ini che è la configurazione della simulazione, generata dal file ini.mako che si basa a sua volta sul file .ned (struttura della simulazione coi parametri - infatti senza quest'ultimo non va).*

NOTA: Prima bisogna sempre eseguire il comando . setenv nella directory omnetpp[versione]/

Scelgo quale simulazione lanciare e la lancio poi velocizzo il tempo di simulazione con il tasto con le tre freccie in alto a sinistra

2) **USO MAKEFILE E SIMULAZIONI MULTIPLE DA LINEA DI COMANDO**

Assicurati che sia presente lo script run; se non c'è, crealo:
```bash
    #!/bin/sh
    cd 'dirname $0'
    ./queuenet $*
```
Creo il makefile con lo scritp python apposito

`make_runfile.py -f [filesimulazione].ini`

Oppure, se è presente nella cartella anche lo script .sh va bene

`./make_runfile.sh [filesimulazione].ini`

Eseguo le simulazioni da linea di comando ed in parallelo (l'argomento j[numero] specifica il numero di jobs in parallelo)

make -j8 -f Runfile

------------

B) **AGGREGAZIONE E ANALISI DATI**

Ora i dati prodotti, impostati tramite il [filesimulazione].ini sono nella cartella  omnetpp[versione]/samples/queuenet/results/
ma sono difficili da processare.
Per questo c'è uno script python che ci aiuta.
Lo scritp prende come file di configurazione un file .json (esempio: configMM1.json) che dentro ha un dizionario con i dati selezionati da raccogliere e il possibile tipo di aggregazione da fare.

Quando si esegue lo script, si crea un file .db che ha al suo interno i dati raccolti!

Una volta settato il file .json, si esegue il comando:

```bash
parse_data.py -c [fileconfig].json -d [nomedbsimulazione].db \
-j[num_processi_paralleli] -r results/[nomesimulazione_*-#*].sca -> occhio qui, deve fare match solo con i run non base altrimenti lo script da un errore out of range!
```
c'è una wildcard * sul file del nomesimulazione (devi evitare i file che hanno la scritta *base* presente nel nome!). 
Prima di eseguire il comando vedere bene se si va a fare match con i file .sca presenti in omnetpp[versione]/samples/queuenet/results/

ad esempio:
```bash
parse_data.py -c configMM1.json -d MM1.db \
-j8 -r results/MM1_*-#0.sca
```
Il comando sopra prende il file configMM1.json per capire quali dati considerare e come aggregarli, carica i dati di tutti i file in results che fanno match con MM1_[numero_simulazione]-#0.sca e processa i dati che inserisce in MM1.db


Per eseguire l'analisi dati sui dati presenti nel db ottenuto, si utilizza lo script analyze_data.py che va a vedere la seconda parte "analyses" del file di configurazione [fileconfig].json!
le varie aggregazioni che possiamo fare sono none, std, avg, sum.

`analyze_data.py -c [fileconfig].json -d [nomedbsimulazione].db`

successivamente i dati saranno salvati in uno o più files in omnetpp[versione]/samples/queuenet/results/*.data
I dati hanno colonne per le varie metriche.
Per ogni metriche è mostrato il valore medio sui vari runs dello stesso scenario con la deviazione standard!

esempio: 

`analyze_data.py -c configMM1.json -d MM1.db`


Si possono anche creare plot con gnuplot.

Si vedano gli esempi /samples/queuenet/MM1.gnuplot


```bash
#!/bin/bash

nome_sim=$1

if [ -z "$nome_sim" ]; then
  echo "È necessario specificare il nome della simulazione."
  exit 1
fi

make_runfile.py -f $nome_sim.ini

make -j 8 -f Runfile

parse_data.py -c config$nome_sim.json -d $nome_sim.db \
    -j8 -r results/${nome_sim}_*-#0.sca

analyze_data.py -c config${nome_sim}.json \
    -d $nome_sim.db
```