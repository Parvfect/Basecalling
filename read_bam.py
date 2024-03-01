
""" Seems to work only on UNIX Files though """

# I'd look at - https://labs.epi2me.io/notebooks/Introduction_to_SAM_and_BAM_files.html

import pysam
import numpy as np
import pandas as pd

read_lengths = []
reads = []


with pysam.AlignmentFile("calls.bam", "rb", check_sq=False) as bam:
    print(bam.header)
    for read in bam.fetch(until_eof=True):
        read_arr = str(read).split()

        # The 9th element is the Sequence
        reads.append(read_arr[9])
    
def motif_search(basepair_strings, motif_length):
    """ Searches for motif of length motif_length and returns the motifs with greatest frequency """

    motif_frequency_dict = {}
    for basepairs in basepair_strings:
        intervals = int(len(basepairs)/motif_length)
        split_arr = [basepairs[i:i+motif_length] for i in range(intervals)]
        for i in split_arr:
            if i in motif_frequency_dict:
                motif_frequency_dict[i] += 1
            else:
                motif_frequency_dict[i] = 1
    return motif_frequency_dict


print(len(reads))
print(len(reads[0]))

dicta = {"A":1, "C":2, "T":3, "G":4}

t = reads.copy()
t = [[dicta[j] for j in i] for i in t]

arr = [0,0,0,0]
for i in t:
    for j in i:
        arr[j-1] +=1

basepair_string = ""
for i in reads[:3]:
    basepair_string = basepair_string.join(i)


motif_dict = motif_search(reads, 5)

# I want to see only the ones over say an arbitary number
threshold = 500
new_motif_dict = {i:motif_dict[i] for i in motif_dict if motif_dict[i]> threshold}

print(new_motif_dict)
# What if we go over all the base pairs and kind of increase the dictionary as we traverse