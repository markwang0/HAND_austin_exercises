#!/usr/bin/env bash

# run crop_inun.py in each HUC8 directory
# HUC8 directories of interest begin with 12*
# activate gis-env conda environment first

for D in 12*; do
    if [ -d "${D}" ]; then
        cd "${D}"
        mkdir -p inundation/mod{1,2a,2b,3a,3b}
        cp ../calc_inun.py .
        python calc_inun.py
        echo "${D} done"
        date
        cd ..
    fi
done
