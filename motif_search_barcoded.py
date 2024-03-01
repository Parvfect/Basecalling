
import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\Parv\Doc\HelixWorks\Basecalling\data\helixworks_1280_fast5_2024-02-09_1638\motif_search_barcoded.csv")


barcodes = [int(i[-2:]) for i in df['ONT_Barcode']]
df['barcodes'] = barcodes

barcodes_T1 =  np.arange(1, 80, 4)
barcodes_T2 =  np.arange(2, 80, 4)
barcodes_T3 =  np.arange(3, 80, 4)
barcodes_T4 =  np.arange(4, 80, 4)


df_consensus = df.loc[df['barcodes'].isin(barcodes_T1)]
read_ids_barcode = {}
reads_ids_hw_address = {}



for j in df_consensus['barcodes'].unique():
    for i in df_consensus['HW_Address'].unique():
        cycle = df.loc[df['HW_Address'] == i]
        reads_ids_hw_address[i] = cycle['read_id'].to_numpy()
    read_ids_barcode[j] = reads_ids_hw_address
