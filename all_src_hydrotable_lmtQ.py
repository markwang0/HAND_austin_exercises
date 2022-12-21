import pandas as pd
from glob import glob

ht_paths=glob('./12*/hydroTable_rp_bf_lmtdischarge_cda.csv')
pd.concat([pd.read_csv(p) for p in ht_paths]).to_csv(
    "hydroTable_all_rp_bf_lmtdischarge_cda.csv.csv", index=False
)
