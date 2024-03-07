

from motif_search_barcoded import get_read_ids_for_consensus
import pandas as pd
import numpy as np
from fast5_readfile_database import get_squiggle_from_read_id
import os
import matplotlib.pyplot as plt
from tqdm import tqdm



def trying():
    fast5_path = r"C:\Users\Parv\Doc\HelixWorks\Basecalling\data\helixworks_1280_fast5_2024-02-09_1638\1280_FAST5"

    # Read_ids_barcoded
    read_ids_barcode_df = pd.read_pickle("read_id_barcoded.pkl")

    # Read_ids per file
    read_id_fast5 = pd.read_pickle("read_id_fast5.pkl")


    squiggles = []

    # for read in read_ids_barcoded
    for read in tqdm(read_ids_barcode_df['read_id']):
        try:
            row = read_id_fast5.loc[read_id_fast5['read_id'] == read]
            filename = row['filename'].to_numpy()[0]
            filename = os.path.join(fast5_path, filename)
            squiggle = get_squiggle_from_read_id(read, filename)
            squiggles.append(squiggle)
        except:
            read_ids_barcode_df.drop(read_ids_barcode_df[read_ids_barcode_df["read_id"]==read].index)
            print("Some bullcrap error")
        


    read_ids_barcode_df["squiggle"] = squiggles
    plt.plot(squiggles[6])
    plt.show()
        
    # Check which file has that read
    # Extract that squiggle from that file
    # Add to squiggles arr
    # Make it last column of df
    # Save df to pickle to create the dataset

    # And then the label becomes for each ONT Barcode and HW address conjugate
    # May take ages not going to lie

def pickling():
    squiggle_df = pd.read_pickle("squiggle_database.pkl")
    squiggles = []
    total_squiggles = 0

    read_ids_barcode_df = pd.read_pickle("read_id_barcoded.pkl")
    read_ids_barcode_df_min = read_ids_barcode_df.head(100)

    print(squiggle_df.head())

    for read in tqdm(read_ids_barcode_df_min['read_id']):
        try:
            row = squiggle_df.loc[squiggle_df['read_id'] == read]
            squiggles.append(row['squiggle'].to_numpy())
            total_squiggles +=1
        except:
            read_ids_barcode_df_min.drop(read_ids_barcode_df_min[read_ids_barcode_df_min["read_id"]==read].index)
            print("Some bullcrap error")
        

    print(total_squiggles)
    read_ids_barcode_df_min["squiggle"] = squiggles
    plt.plot(squiggles[6])
    plt.show()
    read_ids_barcode_df_min.to_csv("Database.csv")
    

pickling()
