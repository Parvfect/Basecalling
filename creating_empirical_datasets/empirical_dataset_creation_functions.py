
from tqdm import tqdm
import pandas as pd
import os
from ont_fast5_api.fast5_interface import get_fast5_file
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def library_motif_segregation(df):
    library_motifs = df['library_motif'].to_numpy()
    library_motifs_arr = []
    no_motifs = []
    for i in library_motifs:
        motifs_arr = i.split('|')
        library_motifs_arr.append(motifs_arr)
        no_motifs.append(len(motifs_arr))
    return library_motifs_arr, no_motifs


# Load encoded csv
# Choose Barcodes (/division of data for train and test)

# Get best quality reads
def get_best_quality_reads(df, ont_barcode, hw_address, n_motifs=6):

    df_subset = df[(df['ONT_Barcode'] == ont_barcode) &
                   (df['HW_Address'] == hw_address) &
                   (df['motifs_discovered'] > n_motifs)]

    read_ids = df_subset['read_id'].to_numpy()
    library_motifs_arr = df_subset['library_motifs_arr'].to_numpy()
    return read_ids, library_motifs_arr


def extract_best_reads(train_barcodes, encoded_train_df):
    training_arr = []

    for barcode in tqdm(train_barcodes):
        for hw_address in tqdm(encoded_train_df['HW_Address'].unique()):
            read_ids, library_motifs_arr = get_best_quality_reads(barcode, hw_address)
            payload = encoded_train_df[(encoded_train_df['ONT_Barcode'] == barcode) & (
                encoded_train_df['HW_Address'] == hw_address)]['Payload'].to_numpy()[0]
            for i, read_id in enumerate(read_ids):
                training_arr.append([
                    barcode, hw_address, payload, library_motifs_arr[i], read_id])          
    return pd.DataFrame(
        training_arr, columns=['ONT_Barcode', 'HW_Address', 'Payload', 'Library_Motifs', 'read_id'])


def extract_fast5_data(fast5_path, target_read_ids):

    total_files = len(os.listdir(fast5_path))
    file_number = 0

    squiggles = {}

    # Trying to see if I can get 10 percent of the reads and have some form of a database
    for file in os.listdir(fast5_path):
        file_number += 1

        # Printing the progress
        if file_number % 10 == 0:
            print(file_number/total_files)

        filepath = os.path.join(fast5_path, file)
        with get_fast5_file(filepath, mode="r") as f5:
            read_ids = f5.get_read_ids()
            read_ids = list(set(read_ids).intersection(target_read_ids))

            for read_id in read_ids:
                read = f5.get_read(read_id)
                squiggle = read.get_raw_data()
                squiggles[read_id] = squiggle

    return squiggles


def normalise_data(df, column_name):

    scaler = MinMaxScaler()
    # Normalize the squiggle data
    return df[column_name].apply(
        lambda x: scaler.fit_transform(np.array(x).reshape(-1, 1)).reshape(-1))


def extract_cycle_motif(library_motif):

    if library_motif[6] == 'x':
        cycle_number = int(library_motif[5])
        motif_number = int(library_motif[7])
    else:
        cycle_number = int(library_motif[5:7])
        motif_number = int(library_motif[8])

    return cycle_number, motif_number


def create_spacer_sequence(library_motifs):

    cycle_number = 0
    motif_number = 0

    spacer_sequence = []

    for i in library_motifs:

        cycle_number, motif_number = extract_cycle_motif(i)

        # So we add a prior spacer and then a post spacer, cause that's what a motif is
        spacer_sequence.append(cycle_number + 8)
        spacer_sequence.append(motif_number)
        spacer_sequence.append(cycle_number + 8)

        if i == 1:
            motif_number += 1
        else:
            cycle_number += 1

    return spacer_sequence


def create_payload_spacer_sequence(payload):

    payload_sequence = []

    cycle_number = 11

    if payload.isinstance(str):
        payload = eval(payload)

    for i in payload:
        for j in i:
            payload_sequence.append(cycle_number)
            payload_sequence.append(j)
            payload_sequence.append(cycle_number)
        cycle_number+=1

    return payload_sequence
