
import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle

df = pd.read_csv(r"C:\Users\Parv\Doc\HelixWorks\Basecalling\data\helixworks_1280_fast5_2024-02-09_1638\motif_search_barcoded.csv")


def get_read_ids_for_consensus():

    barcodes = [int(i[-2:]) for i in df['ONT_Barcode']]
    df['barcodes'] = barcodes

    barcodes_T1 =  np.arange(1, 80, 4)
    barcodes_T2 =  np.arange(2, 80, 4)
    barcodes_T3 =  np.arange(3, 80, 4)
    barcodes_T4 =  np.arange(4, 80, 4)


    df_consensus = df.loc[df['barcodes'].isin(barcodes_T1)]
    read_ids_barcode = {}
    reads_ids_hw_address = {}
    ONT_Barcode = []
    HW_Address = []
    read_ids = []

    for j in tqdm(df_consensus['barcodes'].unique()):
        for i in tqdm(df_consensus['HW_Address'].unique()):
            cycle = df.loc[df['HW_Address'] == i]['read_id'].to_numpy()
            for read_id in cycle:
                ONT_Barcode.append(j)
                HW_Address.append(i)
                read_ids.append(read_id)
    
    read_ids_barcode_df = pd.DataFrame()

    read_ids_barcode_df['ONT_Barcode'] = ONT_Barcode
    read_ids_barcode_df['HW_Address'] = HW_Address
    read_ids_barcode_df['read_id'] = read_ids
    
    return read_ids_barcode_df


#read_ids_barcode_df = get_read_ids_for_consensus()

#read_ids_barcode_df.to_pickle("read_id_barcoded.pkl")

read_ids_barcode_df = pd.read_pickle("read_id_barcoded.pkl")

# Collect Squiggles and then do the information gathering