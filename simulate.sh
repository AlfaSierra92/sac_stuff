# Per eseguire la simulazione via makefile senza eseguire tutta la pappardella a mano.
# Eseguire con: ./simulate.sh nome_simulazione

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
