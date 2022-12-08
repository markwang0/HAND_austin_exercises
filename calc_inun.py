import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio as rio


module1_df = pd.read_csv(
    "../AustinExerciseModules/module1_stage_flow_15Oct2022_4pm_predicted_peak_flow.csv"
)

module2a_df = pd.read_csv(
    "../AustinExerciseModules/module2a_stage_flow_nwm.t15z.analysis_assim.channel_rt.tm00.aus_txdot.csv"
)

module2b_df = pd.read_csv(
    "../AustinExerciseModules/module2b_stage_flow_nwm.t15z.short_range.channel_rt.f006.aus_txdot.csv"
)

module3a_df = pd.read_csv(
    "../AustinExerciseModules/module3a_stage_flow_nwm.20181018_flow.analysis_assim_t15z.channel_rt.tm00.aus_txdot.csv"
)

module3b_df = pd.read_csv(
    "../AustinExerciseModules/module3b_stage_flow_nwm.20181014_20181019_peakflow.analysis_assim.channel_rt.tm00.aus_txdot.csv"
)

# Llano HUC8 FATSGTID domain
llano_min_fatsgtid = 25040001
llano_max_fatsgtid = 25043349

mod_dfs_temp = [
    module1_df,
    module2a_df,
    module2b_df,
    module3a_df,
    module3b_df,
]

catch_df = gpd.read_file(
    "gw_catchments_reaches_filtered_addedAttributes_crosswalked.gpkg",
    layer='gw_catchments_reaches_filtered_addedAttributes_crosswalked',
)

# keep only those FATSGTIDs present in this HUC8
mod_dfs = []
for mod_df in mod_dfs_temp:
    mod_df = mod_df[mod_df['FATSGTID'].isin(catch_df['HydroID'])]
    mod_dfs.append(mod_df)

for (mod_df, name) in zip(
    mod_dfs, ["mod1", "mod2a", "mod2b", "mod3a", "mod3b"]
):
    for fatsgtid in mod_df["FATSGTID"]:
        if len(mod_df["stage_m"].loc[mod_df["FATSGTID"] == fatsgtid]) != 0:
            stage = (
                mod_df["stage_m"].loc[mod_df["FATSGTID"] == fatsgtid].item()
            )
            for (fpath, heal_status) in zip(
                    ["hand_FATSGTID_", "hand_healed_FATSGTID_"],
                    ["unhealed","healed"]
                ):
                with rio.open(f"cropped_hand/{fpath}{fatsgtid}.tif") as src:
                    hand = src.read(1, masked=True)
                    profile = src.profile
                # set inundation to 0 for nodata (-9999) and hand >= stage
                # otherwise inundation is stage minus hand
                inun = np.where((hand >= stage) | (hand < 0), 0, stage - hand)
                inun = np.ma.masked_where(inun == 0, inun)  # mask out 0 inundation
                # save mask with GDAL convention
                msk = (~inun.mask * 255).astype("uint8")
                with rio.Env(GDAL_TIFF_INTERNAL_MASK=True):
                    with rio.open(
                        f"inundation/{name}/{heal_status}_inun_{fatsgtid}.tif", "w", **profile
                    ) as ds_out:
                        ds_out.write(inun, 1)
                        if isinstance(msk, np.uint8):
                            continue
                        else:
                            ds_out.write_mask(msk)


