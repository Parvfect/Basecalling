
from ont_fast5_api.fast5_interface import get_fast5_file
import pandas as pd
import numpy as np

def print_all_raw_data(filepath):
    data = []
    with get_fast5_file(filepath, mode="r") as f5:
        for read in f5.get_reads():
            raw_data = read.get_raw_data()
            data.append(raw_data)
    
    return data

filepath = r"C:\Users\Parv\Doc\HelixWorks\Basecalling\data\tut.fast5"

data_seq = np.load("data_seq.npy")
