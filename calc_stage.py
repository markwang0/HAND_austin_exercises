import numpy as np
import os
import pandas as pd

# read in corrected streamflows for Llano HUC8 module 1
mod1_comids_q_df = pd.read_excel(
    "./AustinExerciseModules_rev/HAND_streams_output_TableToExcel.xlsx",
    usecols=["HydroID", "DischargeCMS"],
)
mod1_comids_q_df.index = mod1_comids_q_df["HydroID"]
mod1_comids_q_df = mod1_comids_q_df.drop(columns="HydroID")

# read in synthetic rating curves for Llano HUC8 from Yan
llano_hydrotable = pd.read_csv(
    "12090204/hydroTable.csv",
    usecols=["HydroID", "stage", "discharge_cms"],
)
llano_hydrotable.index = llano_hydrotable["HydroID"]
llano_hydrotable = llano_hydrotable.drop(columns="HydroID")

# interpolate stage from streamflows with synthetic rating table
mod1_comids_q_df["stage"] = np.nan
for hydroid in mod1_comids_q_df.index:
    # for each HydroID, subset hydrotable.csv
    # to get the HydroID specific rating table 
    # and interpolate stage from discharge
    stage = np.interp(
        mod1_comids_q_df.loc[hydroid, "DischargeCMS"],
        llano_hydrotable.loc[hydroid, "discharge_cms"],
        llano_hydrotable.loc[hydroid, "stage"],
    )
    mod1_comids_q_df.loc[hydroid,'stage'] = stage

# save file with interpolated stage values
mod1_comids_q_df.to_csv(
    "12090204/mod1_rev.csv",
)



