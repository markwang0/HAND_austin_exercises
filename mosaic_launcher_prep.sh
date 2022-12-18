#!/usr/bin/env bash

# make subdirectories for inudnation .tif files
# create file of launcher commands

if [ -f mosaic_launcher.sh ]; then
    rm mosaic_launcher.sh
fi

mods=("1 2a 2b 3a 3b")
for D in 12*; do
    if [ -d "${D}" ]; then
        for i in ${mods[@]}; do
            if [ -d "${D}"/inundation_rev/mod"${i}" ]; then
                echo "gdalwarp -dstnodata -9999 \
-srcnodata -9999 \
-co \"COMPRESS=LZW\" \
-multi \
${D}/inundation_rev/mod${i}/healed_*.tif \
mosaic/${D}_mod${i}_healed_mosaic.tif" >> mosaic_launcher.sh
                echo "gdalwarp -dstnodata -9999 \
-srcnodata -9999 \
-co \"COMPRESS=LZW\" \
-multi \
${D}/inundation_rev/mod${i}/unhealed_*.tif \
mosaic/${D}_mod${i}_unhealed_mosaic.tif" >> mosaic_launcher.sh
            fi
        done
    fi
done

