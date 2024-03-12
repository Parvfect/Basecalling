

import pandas as pd

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


    
