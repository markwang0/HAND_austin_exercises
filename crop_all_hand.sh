#!/usr/bin/env bash

# run crop_hand.py in each HUC8 directory
# HUC8 directories of interest begin with 12*
# activate gis-env conda environment first

for D in 12*; do
    if [ -d "${D}" ]; then
        cd "${D}"
        cp ../crop_hand.py .
        python crop_dem.py
        echo "${D} done"
        cd ..
    fi
done
