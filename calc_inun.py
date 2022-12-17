import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio as rio
import sys

module1_df = pd.read_csv("./AustinExerciseModules_rev/mod1_stage.csv")
module2a_df = pd.read_csv("./AustinExerciseModules_rev/mod2a_stage.csv")
module2b_df = pd.read_csv("./AustinExerciseModules_rev/mod2b_stage.csv")
module3a_df = pd.read_csv("./AustinExerciseModules_rev/mod3a_stage.csv")
module3b_df = pd.read_csv("./AustinExerciseModules_rev/mod3b_stage.csv")

mod_dfs_temp = [
    module1_df,
    module2a_df,
    module2b_df,
    module3a_df,
    module3b_df,
]

# pass HUC8 name (subdirectory name) as command line argument
huc8_path = sys.argv[1]

catch_df = gpd.read_file(
    f"{huc8_path}/gw_catchments_reaches_filtered_addedAttributes_crosswalked.gpkg",
    layer="gw_catchments_reaches_filtered_addedAttributes_crosswalked",
)

# keep only those HydroIDs present in this HUC8 (HydroID == FATSGTID)
mod_dfs = []
for mod_df in mod_dfs_temp:
    mod_df = mod_df[mod_df["HydroID"].isin(catch_df["HydroID"])]
    mod_dfs.append(mod_df)

for (mod_df, name) in zip(
    mod_dfs, ["mod1", "mod2a", "mod2b", "mod3a", "mod3b"]
):
    for hydroid in mod_df["HydroID"]:
        if len(mod_df["stage_m"].loc[mod_df["HydroID"] == hydroid]) != 0:
            stage = mod_df["stage_m"].loc[mod_df["HydroID"] == hydroid].item()
            for (fpath, heal_status) in zip(
                ["hand_FATSGTID_", "hand_healed_FATSGTID_"],
                ["unhealed", "healed"],
            ):
                with rio.open(
                    f"{huc8_path}/cropped_hand/{fpath}{hydroid}.tif"
                ) as src:
                    hand = src.read(1, masked=True)
                    profile = src.profile
                # set inundation to 0 for nodata (-9999) and hand >= stage
                # otherwise inundation is stage minus hand
                inun = np.where((hand >= stage) | (hand < 0), 0, stage - hand)
                inun = np.ma.masked_where(
                    inun == 0, inun
                )  # mask out 0 inundation
                # save mask with GDAL convention
                msk = (~inun.mask * 255).astype("uint8")
                with rio.Env(GDAL_TIFF_INTERNAL_MASK=True):
                    with rio.open(
                        f"{huc8_path}/inundation/{name}/{heal_status}_inun_{hydroid}.tif",
                        "w",
                        **profile,
                    ) as ds_out:
                        ds_out.write(inun, 1)
                        if isinstance(msk, np.uint8):
                            continue
                        else:
                            ds_out.write_mask(msk)
