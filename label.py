
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

decoded_consensus_df = pd.read_csv("decoded_consensus.tsv", sep='\t') # This is the decoded consensus 
squiggle_database_df = pd.read_pickle("squiggle_database.pkl") # All the reads with the squiggles
read_id_barcoded_df = pd.read_pickle("read_id_barcoded.pkl") # Read ids and their barcodes

print(decoded_consensus_df.head())
print(squiggle_database_df.head())
print(read_id_barcoded_df.head())

""" For Each Unique ONT Barcode and HW_Address pair - how many read ids do we have?
ont_unique = read_id_barcoded_df['ONT_Barcode'].unique()
hw_address_unique = read_id_barcoded_df['HW_Address'].unique()

for i in ont_unique:
    for j in hw_address_unique:
        df = read_id_barcoded_df.loc[(read_id_barcoded_df['ONT_Barcode'] == i) & (read_id_barcoded_df['HW_Address'] == j)]
        print(df.shape[0])

About 8000 reads per unique pair of ONT and HW, can select like 100 to begin with to see how our model does 
"""


def get_label(ONT_Barcode, HW_Address):
    label_row = decoded_consensus_df.loc[(decoded_consensus_df['ONT_Barcode'] == ONT_Barcode) & (decoded_consensus_df['HW_address'] == HW_Address)]
    payload_columns = label_row.columns[2:]
    label = [label_row[i].to_numpy()[0] for i in payload_columns]
    label_str = ""
    for i in label:
        label_str += " " +i
    
    return label_str.replace('[', '').replace(']', '').replace(',', '')

def get_read_id(ONT_Barcode, HW_Address, sample_length=10):
    read_id_rows = read_id_barcoded_df.loc[(read_id_barcoded_df['ONT_Barcode'] == ONT_Barcode) & (read_id_barcoded_df['HW_Address'] == HW_Address)]
    read_ids = read_id_rows['read_id'].to_numpy()
    samples = [np.random.choice(len(read_ids)) for i in range(sample_length)]
    return read_ids[samples]

def get_squiggle(read_id):
    return squiggle_database_df.loc[squiggle_database_df['read_id'] == read_id]['squiggle'].to_numpy()
    

labels = []
ont_unique = read_id_barcoded_df['ONT_Barcode'].unique()
hw_address_unique = read_id_barcoded_df['HW_Address'].unique()

onts = []
hws = []
squiggles = []

for i in tqdm(ont_unique):
    for j in hw_address_unique:
        label = get_label(i,j)
        
        read_id = get_read_id(i,j, sample_length=1)
        squiggle = get_squiggle(read_id[0])
        squiggles.append(squiggle)
        onts.append(i)
        hws.append(j)
    

dataset_df = pd.DataFrame()
dataset_df['ONT_Barcode'] = onts
dataset_df['HW_Address'] = hws
dataset_df['squiggle'] = squiggles
dataset_df['label'] = label

print(dataset_df.head())

dataset_df.to_pickle("dataset.pkl")
