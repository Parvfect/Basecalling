
# Getting the metadata from the fast5 which will help me see what the fastq corresponds to 

from ont_fast5_api.fast5_interface import get_fast5_file
import os
import matplotlib.pyplot as plt
import json
import pickle
import pandas as pd
from tqdm import tqdm


def extract_squiggle_dict_from_fast5(fast5_file):
    """Goes through a fast5 file and returns read_id indexed squiggles as a dict

        Args:
            fast5_file (path): Path to the fast5 file
        Returns:
            squiggles (dict): read id indexed squiggles as numpy arrays
    """

    squiggles = {}

    with get_fast5_file(fast5_file, mode="r") as f5:
        for read_id in f5.get_read_ids():
            read = f5.get_read(read_id)
            squiggle = read.get_raw_data()
            # Process the squiggle data here
            squiggles[read_id] = squiggle

    return squiggles

def extract_squiggles_from_fast5(fast5_file):
    """Goes through a fast5 file and returns read_id indexed squiggles as a dict

        Args:
            fast5_file (path): Path to the fast5 file
        Returns:
            squiggles (dict): read id indexed squiggles as numpy arrays
    """

    squiggles = []
    read_ids = []

    with get_fast5_file(fast5_file, mode="r") as f5:
        for read_id in f5.get_read_ids():
            read = f5.get_read(read_id)
            squiggle = read.get_raw_data()
            # Process the squiggle data here
            read_ids.append(read_id)
            squiggles.append(squiggle)

    return read_ids, squiggles



def extract_read_ids_from_fast5(fast5_file):
    """Extracts all the read ids from the fast5 file

        Args:
            fast5_file (path): Path to the fast5 file
        Returns:
            read_ids (arr): Array with all the readids
    """

    read_ids = []

    with get_fast5_file(fast5_file, mode="r") as f5:
        for read_id in f5.get_read_ids():
            read_ids.append(read_id)
            #squiggle = f5.get_read(read_id).get_raw_data()
            #print(squiggle)

    return read_ids

def get_squiggles_from_read_ids(read_ids, fast5_file):
    """Returns Squiggle array for read_ids

        Args:
            read_ids (arr): Array of read ids in fast5
            fast5_file (path): Path to the fast 5 file
        Returns:
            squiggle (arr): Read Id indexed Squiggle arr
    """
    
    squiggle = []
    with get_fast5_file(fast5_file, mode="r") as f5:
        for i in read_ids:
            try:
                squiggle.append(f5.get_read(i).get_raw_data())
            except:
                print(f"Read id {i} not in file")

    return squiggle


def get_squiggle_from_read_id(read_id, fast5_file):
    """Returns Squiggle array for read_ids

        Args:
            read_id (str): Readid
            fast5_file (path): Path to the fast 5 file
        Returns:
            squiggle (arr): Squiggle arr
    """
    
    squiggle = []
    with get_fast5_file(fast5_file, mode="r") as f5:
        try:
            read = f5.get_read(read_id)
            squiggle = read.get_raw_data()
            return squiggle
        except:
            print(f"Read id {read_id} not in file")
            return None

general_path = r"C:\Users\Parv\Doc\HelixWorks\Basecalling\data\helixworks_1280_fast5_2024-02-09_1638\1280_FAST5\FAX73317_5becdbe5_a0e99884_6.fast5"

#read_ids = extract_read_ids_from_fast5(general_path)
#squiggle = get_squiggles_from_read_ids(read_ids, general_path)

def create_pkl():
    fast5_path = r"C:\Users\Parv\Doc\HelixWorks\Basecalling\data\helixworks_1280_fast5_2024-02-09_1638\1280_FAST5"

    # Go through all the files in the directory and extract their read_ids
    read_id_database = []
    read_ids = []
    files = []
    counter = 0

    for file in tqdm(os.listdir(fast5_path)[:580]):    
        filepath = os.path.join(fast5_path, file)
        read_ids_local = extract_read_ids_from_fast5(filepath)
        for read_id in read_ids_local:
            files.append(file)
            read_ids.append(read_id)
            print(get_squiggle_from_read_id(read_id, filepath))

    read_id_df = pd.DataFrame()

    read_id_df["filename"] = files
    read_id_df["read_id"] = read_ids

    filepath = os.path.join(fast5_path, files[10])
    print(read_ids[10])
    squiggle = get_squiggles_from_read_ids([read_ids[10]], filepath)
    print(squiggle)

    #read_id_df.to_pickle("read_id_fast5.pkl", index=False)

def create_squiggle_pkl():
    fast5_path = r"C:\Users\Parv\Doc\HelixWorks\Basecalling\data\helixworks_1280_fast5_2024-02-09_1638\1280_FAST5"

    # Go through all the files in the directory and extract their read_ids
    read_id_database = []
    squiggle_database = []
    files = []
    counter = 0

    # Trying to see if I can get 10 percent of the reads and have some form of a database
    for file in tqdm(os.listdir(fast5_path)[:80]):    
        filepath = os.path.join(fast5_path, file)
        read_ids, squiggles = extract_squiggles_from_fast5(filepath)

        read_id_database += read_ids
        squiggle_database += squiggles


    
    df = pd.DataFrame()
    df['read_id'] = read_id_database
    df['squiggle'] = squiggle_database

    df.to_pickle("squiggle_database.pkl")

    return


def fast5_creation():
    """Automatically create by checking if those reads are in the barcoded reads and then extracting those relevant squiggles"""

    fast5_path = r"C:\Users\Parv\Doc\HelixWorks\Basecalling\data\helixworks_1280_fast5_2024-02-09_1638\1280_FAST5"
    read_ids_barcode_df = pd.read_pickle("read_id_barcoded.pkl")
    print(read_ids_barcode_df.head())
    read_ids_barcoded = read_ids_barcode_df['read_id'].to_numpy()

    # Go through all the files in the directory and extract their read_ids
    read_id_database = []
    squiggle_database = []
    ont = []
    hw = []
    counter = 0

    # Trying to see if I can get 10 percent of the reads and have some form of a database
    for file in tqdm(os.listdir(fast5_path)[:10]):    
        filepath = os.path.join(fast5_path, file)
        with get_fast5_file(filepath, mode="r") as f5:
            read_ids = f5.get_read_ids()
            read_ids = list(set(read_ids).intersection(read_ids_barcoded))
            
            for read_id in (read_ids):
                read_id_database.append(read_id)
                read = f5.get_read(read_id)
                squiggle_database.append(read.get_raw_data())
            
    
    df = pd.DataFrame()
    df['read_id'] = read_id_database
    df['squiggle'] = squiggle_database
    ont = []
    hw = []
    print(df.head())

    for i in tqdm(read_id_database):
        row = read_ids_barcode_df.loc(read_ids_barcode_df['read_id'] == i)
        ont.append(row['ONT_Barcode'])
        hw.append(row['HW_Address'])

    print(df.head())

    #df.to_pickle("squiggle_database.pkl")


if __name__ == "__main__":
    fast5_creation()
