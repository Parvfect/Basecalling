
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
data = print_all_raw_data(filepath)


data_seq = []
for i in data:
    for j in i:
        data_seq.append(j)

data_seq = np.array(data_seq)

# convert to dataframe in 50 columns
#df = pd.DataFrame(data_seq)

n = 20
  
# using list comprehension 
data_arr = [data_seq[i * n:(i + 1) * n] for i in range((len(data_seq) + n - 1) // n )]  
print(data_arr)
