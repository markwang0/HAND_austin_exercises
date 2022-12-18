#!/usr/bin/env bash

# make subdirectories for inudnation .tif files
# create file of launcher commands

if [ -f full_mosaic_launcher.sh ]; then
    rm full_mosaic_launcher.sh
fi

mods=("1 2a 2b 3a 3b")

for i in ${mods[@]}; do
    echo "gdalwarp -dstnodata -9999 \
-srcnodata -9999 \
-co \"COMPRESS=LZW\" \
mosaic/*_mod${i}_healed_mosaic.tif \
full_mosaic/mod${i}_healed_full_mosaic.tif" >> full_mosaic_launcher.sh
    echo "gdalwarp -dstnodata -9999 \
-srcnodata -9999 \
-co \"COMPRESS=LZW\" \
mosaic/*_mod${i}_unhealed_mosaic.tif \
full_mosaic/mod${i}_unhealed_full_mosaic.tif" >> full_mosaic_launcher.sh
done
