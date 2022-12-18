#!/usr/bin/env bash

module load launcher
export OMP_NUM_THREADS=2 # -multi option on gdalwarp
export LAUNCHER_WORKDIR=${pwd}
export LAUNCHER_JOB_FILE=${pwd}/mosaic_launcher.sh
$LAUNCHER_DIR/paramrun

