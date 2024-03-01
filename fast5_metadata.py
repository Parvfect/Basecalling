

# Getting the metadata from the fast5 which will help me see what the fastq corresponds to 

from ont_fast5_api.fast5_interface import get_fast5_file
import os

general_path = r"C:\Users\Parv\Doc\HelixWorks\Basecalling\data\helixworks_1280_fast5_2024-02-09_1638\1280_FAST5\FAX73317_5becdbe5_a0e99884_6.fast5"

def extract_reads_from_fast5(fast5_file):

    squiggles = {}

    with get_fast5_file(fast5_file, mode="r") as f5:
        for read_id in f5.get_read_ids():
            read = f5.get_read(read_id)
            squiggle = read.get_raw_data()
            # Process the squiggle data here
            squiggles[read_id] = squiggle

    return squiggles

# Replace 'path_to_fast5_file' with the path to your FAST5 file
#read_ids = print_fast5_metadata(general_path)

squiggles = extract_reads_from_fast5(general_path)

print(squiggles)