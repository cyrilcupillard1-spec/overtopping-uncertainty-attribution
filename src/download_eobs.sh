#!/bin/bash
mkdir -p data/raw
cd data/raw
for periode in 1980-1994 1995-2010 2011-2025; do
  curl -C - -O "https://knmi-ecad-assets-prd.s3.amazonaws.com/ensembles/data/Grid_0.1deg_reg_ensemble/rr_ens_mean_0.1deg_reg_${periode}_v33.0e.nc"
done
