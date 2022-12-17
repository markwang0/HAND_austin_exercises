#!/usr/bin/env bash

# make subdirectories for inudnation .tif files
# create file of launcher commands

if [ -f inun_launcher.sh ]; then
    rm inun_launcher.sh
fi

for D in 12*; do
    if [ -d "${D}" ]; then
        mkdir -p ${D}/inundation_rev/mod{1,2a,2b,3a,3b}
        echo "python calc_inun.py \"${D}\"" >> inun_launcher.sh
    fi
done
