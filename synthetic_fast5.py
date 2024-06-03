

from ont_fast5_api.fast5_interface import get_fast5_file

def print_all_raw_data(fast5_filepath):
    raw_data_arr = []
    with get_fast5_file(fast5_filepath, mode="r") as f5:
        for read in f5.get_reads():
            raw_data = read.get_raw_data()
            raw_data_arr.append(raw_data)
    return raw_data_arr


fast5_filepath = r"out_signal.fast5"

raw_data_arr = print_all_raw_data(fast5_filepath)




