#!/bin/bash

for i in {3..15}; do
  if [[ "$i" -eq 3 ]]; then
    simulations=10000
  elif [[ "$i" -eq 4 ]]; then
    simulations=4000
  else
    simulations=1000
  fi
  for j in $(seq 3 $i); do
    date
    echo python src/__main__.py store-ann --ann-model adaptive --dimension 3 --size "$i" --to-win "$j" --simulations "$simulations"
    python src/__main__.py store-ann --ann-model adaptive --dimension 3 --size "$i" --to-win "$j" --simulations "$simulations"
  done
done
