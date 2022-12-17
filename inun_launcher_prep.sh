#!/usr/bin/env bash

# make subdirectories for inudnation .tif files
# create file of launcher commands

rm inun_launcher.sh
for D in 12*; do
    if [ -d "${D}" ]; then
        mkdir -p ${D}/inundation/mod{1,2a,2b,3a,3b}
        echo "python calc_inun.py \"${D}\"" >> inun_launcher.sh
    fi
done
