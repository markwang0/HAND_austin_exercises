import numpy as np
import os
import sys
import pandas as pd

# read in corrected streamflows

module1_df = pd.read_csv(
    "./AustinExerciseModules_rev/module1.csv",
    usecols=["HydroID", "streamflow"],
)
module1_df.index = module1_df["HydroID"]
module1_df.drop(columns="HydroID", inplace=True)

module2a_df = pd.read_csv(
    "./AustinExerciseModules_rev/module2a.csv",
    usecols=["HydroID", "streamflow"],
)
module2a_df.index = module2a_df["HydroID"]
module2a_df.drop(columns="HydroID", inplace=True)

module2b_df = pd.read_csv(
    "./AustinExerciseModules_rev/module2b.csv",
    usecols=["HydroID", "streamflow"],
)
module2b_df.index = module2b_df["HydroID"]
module2b_df.drop(columns="HydroID", inplace=True)

module3a_df = pd.read_csv(
    "./AustinExerciseModules_rev/module3a.csv",
    usecols=["HydroID", "streamflow"],
)
module3a_df.index = module3a_df["HydroID"]
module3a_df.drop(columns="HydroID", inplace=True)

module3b_df = pd.read_csv(
    "./AustinExerciseModules_rev/module3b.csv",
    usecols=["HydroID", "streamflow"],
)
module3b_df.index = module3b_df["HydroID"]
module3b_df.drop(columns="HydroID", inplace=True)

# read in master synthetic rating curves csv
hydrotable = pd.read_csv(
    "./AustinExerciseModules_rev/hydroTable_all.csv",
    usecols=["HydroID", "stage", "discharge_cms"],
)
hydrotable.index = hydrotable["HydroID"]
hydrotable = hydrotable.drop(columns="HydroID")

# interpolate stage from streamflows with synthetic rating table
mod_dfs = [module1_df, module2a_df, module2b_df, module3a_df, module3b_df]
for (mod_df, name) in zip(
    mod_dfs,
    ["mod1", "mod2a", "mod2b", "mod3a", "mod3b"],
):

    mod_df["stage_m"] = np.nan
    for hydroid in mod_df.index:
        # for each HydroID, subset hydrotable.csv
        # to get the HydroID specific rating table
        # and interpolate stage from discharge
        stage = np.interp(
            mod_df.loc[hydroid, "streamflow"],
            hydrotable.loc[hydroid, "discharge_cms"],
            hydrotable.loc[hydroid, "stage"],
        )
        mod_df.loc[hydroid, "stage_m"] = stage

    mod_df.to_csv(
        f"./AustinExerciseModules_rev/{name}_stage.csv",
    )
