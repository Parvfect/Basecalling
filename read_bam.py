
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
        

print(len(reads))
print(len(reads[0]))

dicta = {"A":1, "C":2, "T":3, "G":4}

t = reads.copy()
t = [[dicta[j] for j in i] for i in t]


arr = [0,0,0,0]
for i in t:
    for j in i:
        arr[j-1] +=1
print(arr)
