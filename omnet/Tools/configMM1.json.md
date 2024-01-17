Nello *scenario_schema* metto i parametri che verranno gestiti nell'analisi dei dati.
In questo caso si lavora su K e rho (infatti nel file .ini.mako gli scenari vengono definiti in base a loro variazioni) e quindi li analizzero' essi.
```json
{
    "scenario_schema": {
        "rho": {"pattern": "**.rho", "type": "real"},
        "K": {"pattern": "**.K", "type": "int"}
    },
```
Qui ci sono le metriche: esse sono definite negli oggetti del .ned quali sink e src; servini per l'analisi.
```json
    "metrics": {
        "TotalJobs": {"module": "**.src", "scalar_name": "created:last" ,"aggr": ["none"]},
        "DroppedJobs": {"module": "**.srv", "scalar_name": "dropped:count" ,"aggr": ["none"]},
        "QLen": {"module": "**.srv", "scalar_name": "queueLength:timeavg" ,"aggr": ["none"]},
        "Utilization": {"module": "**.srv", "scalar_name": "busy:timeavg" ,"aggr": ["none"]},
        "PQueue": {"module": "**.sink", "scalar_name": "queuesVisited:mean" ,"aggr": ["none"]},
        "ServiceTime": {"module": "**.sink", "scalar_name": "totalServiceTime:mean" ,"aggr": ["none"]},
        "WaitingTime": {"module": "**.sink", "scalar_name": "totalQueueingTime:mean" ,"aggr": ["none"]},
        "ResponseTime": {"module": "**.sink", "scalar_name": "lifeTime:mean" ,"aggr": ["none"]}
    },
```
**Analyses**: creano i file di output con tutti i dati aggregati nel file *outfile*. Posso suddividere i dati arbitrariamente (qui, ad esempio, per ogni "blocco" fisso K e faccio variare rho, ovviamente quest'ultima sempre in funzione dei valori definiti nel .ini.mako).
```python
%for rho in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.88, 0.9]:
```
-----
```json
    "analyses": {
        "SensRho-Kinf": {
            "outfile": "results/loadcurve_inf.data",
            "scenarios": {
                "fixed": {"K": "-1"},
                "range": ["rho"]
            },
            "metrics": [
                {"metric": "TotalJobs", "aggr": "none"},
                {"metric": "DroppedJobs", "aggr": "none"},
                {"metric": "PQueue", "aggr": "none"},
                {"metric": "ServiceTime", "aggr": "none"},
                {"metric": "WaitingTime", "aggr": "none"},
                {"metric": "ResponseTime", "aggr": "none"}
                    ]
        },
        "SensRho-K10": {
            "outfile": "results/loadcurve_K10.data",
            "scenarios": {
                "fixed": {"K": "10"},
                "range": ["rho"]
            },
            "metrics": [
                {"metric": "TotalJobs", "aggr": "none"},
                {"metric": "DroppedJobs", "aggr": "none"},
                {"metric": "PQueue", "aggr": "none"},
                {"metric": "ServiceTime", "aggr": "none"},
                {"metric": "WaitingTime", "aggr": "none"},
                {"metric": "ResponseTime", "aggr": "none"}
                    ]
        },
        "SensRho-K7": {
            "outfile": "results/loadcurve_K7.data",
            "scenarios": {
                "fixed": {"K": "7"},
                "range": ["rho"]
            },
            "metrics": [
                {"metric": "TotalJobs", "aggr": "none"},
                {"metric": "DroppedJobs", "aggr": "none"},
                {"metric": "PQueue", "aggr": "none"},
                {"metric": "ServiceTime", "aggr": "none"},
                {"metric": "WaitingTime", "aggr": "none"},
                {"metric": "ResponseTime", "aggr": "none"}
                    ]
        },
        "SensRho-K5": {
            "outfile": "results/loadcurve_K5.data",
            "scenarios": {
                "fixed": {"K": "5"},
                "range": ["rho"]
            },
            "metrics": [
                {"metric": "TotalJobs", "aggr": "none"},
                {"metric": "DroppedJobs", "aggr": "none"},
                {"metric": "PQueue", "aggr": "none"},
                {"metric": "ServiceTime", "aggr": "none"},
                {"metric": "WaitingTime", "aggr": "none"},
                {"metric": "ResponseTime", "aggr": "none"}
                    ]
        }
    }
}
```