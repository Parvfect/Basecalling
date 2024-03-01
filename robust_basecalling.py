
import numpy as np
import ast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
import random

def choose_symbols(n_motifs, picks):
    """Creates Symbol Array as a combination of Motifs
    
    Args: 
        n_motifs (int): Total Number of Motifs
        picks (int): Number of Motifs per Symbol
    Returns: 
        symbols (list): List of all the Symbols as motif combinations
    """

    # Reference Motif Address starts from 1 not 0
    return [list(i) for i in (combinations(np.arange(1, n_motifs+1), picks))]

def create_mask(rng, mask_length):
    """ 
    Creates the mask to convert from FF67 to FF70 by mod 70 addition to a psuedo random string
    Takes in the rng seed so we can save our masks
    ----
    Codeword + Mask % 70 = Channel Input
    """
    return [rng.integers(0,70) for i in range(mask_length)]

# Checking which motifs are most robust to basecalling error

def read_payloads_from_file(filename):

    df = pd.read_csv(filename, sep="\t")
    # Getting purely the payload columns
    payloads = df.drop(['ONT_Barcode', 'HW_Address'], axis=1)
    payloads_arr = payloads.to_numpy()
    payloads_arr = np.array([[ast.literal_eval(j) for j in i] for i in payloads_arr])
    payloads_arr = payloads_arr.reshape(10240, 4)
    payloads_arr = payloads_arr[:-16]

    return payloads_arr.reshape(8,1278,4)
   
def unmask_payloads(payloads_arr):
    """Flattens all the way """

    rng = np.random.default_rng(seed=42)

    symbols = choose_symbols(8, 4)
    new_payload_arr = np.zeros([8,1278,4])
    shape = payloads_arr.shape

    for i in range(shape[0]):
        mask = create_mask(rng, 1278)
        for j in range(shape[1]):
            if list(payloads_arr[i,j]) in symbols:
                symbol_read = symbols.index(list(payloads_arr[i,j]))
            else:
                symbol_read = 0 # Mask will rearrange psuedo randomly
            unmasked_symbol = (symbol_read - mask[j]) % 70
            motifs_unmasked = symbols[unmasked_symbol]
            #print(motifs_unmasked)
            new_payload_arr[i,j] = motifs_unmasked

    return new_payload_arr


filenames = {
    'dc99.74':[r"C:\Users\Parv\Doc\HelixWorks\code\data\E1C01-01-1280\OAS\T1-DC-99.74\EIC01-01-1280-T1_encoded.tsv", r"C:\Users\Parv\Doc\HelixWorks\code\data\E1C01-01-1280\OAS\T1-DC-99.74\EIC01-01-1280-T1_decoded_consensus.tsv"],
    'dc60.51':[r"C:\Users\Parv\Doc\HelixWorks\code\data\E1C01-01-1280\OAS\T2-DC-60.51\EIC01-01-1280-T2_encoded.tsv", r"C:\Users\Parv\Doc\HelixWorks\code\data\E1C01-01-1280\OAS\T2-DC-60.51\EIC01-01-1280-T2_decoded_consensus.tsv"],
    'dc33.45':[r"C:\Users\Parv\Doc\HelixWorks\code\data\E1C01-01-1280\OAS\T3 -DC-33.45\EIC01-01-1280-T3_encoded.tsv", r"C:\Users\Parv\Doc\HelixWorks\code\data\E1C01-01-1280\OAS\T3 -DC-33.45\EIC01-01-1280-T3_decoded_consensus.tsv"],
    'dc11.45':[r"C:\Users\Parv\Doc\HelixWorks\code\data\E1C01-01-1280\OAS\T4-DC-11.45\EIC01-01-1280-T4_encoded.tsv", r"C:\Users\Parv\Doc\HelixWorks\code\data\E1C01-01-1280\OAS\T4-DC-11.45\EIC01-01-1280-T4_decoded_consensus.tsv"]
}


encoded_motifs = []
decoded_motifs = []

for i in list(filenames.keys()):
    filename = filenames[i]
    encoded_motifs.append(read_payloads_from_file(filename[0]))
    decoded_motifs.append(read_payloads_from_file(filename[1]))

encoded_motifs = np.array(encoded_motifs)
decoded_motifs = np.array(decoded_motifs)

wrong_motif_counts = []
total_motif_count = np.zeros(8)
total_motif_counts = []
motifs_label = ['1', '2', '3', '4', '5', '6', '7', '8']

for i in range(4):
    unmasked_encoded_motifs = unmask_payloads(encoded_motifs[i])
    unmasked_decoded_motifs = unmask_payloads(decoded_motifs[i])
    
    #unmasked_encoded_motifs = encoded_motifs[i]
    #unmasked_decoded_motifs = decoded_motifs[i]


    unmasked_encoded_file = unmasked_encoded_motifs.reshape(8*1278*4)
    unmasked_decoded_file = unmasked_decoded_motifs.reshape(8*1278*4)

    tmfs = np.zeros(8)
    for i in range(8*1278*4):
        if not unmasked_encoded_file[i] == unmasked_decoded_file[i]:
            motif = int(unmasked_encoded_file[i])
            #print(motif)
            total_motif_count[motif - 1] +=1 # Since labelled 1-8 in HC
            tmfs[motif - 1] += 1
    
    total_motif_counts.append(tmfs)


mean_val = np.mean(total_motif_count)
plt.bar(motifs_label, total_motif_count)
plt.xlabel("Motifs")
plt.ylabel("Errors Per Motif in Sequencing Pipeline")
plt.axhline(mean_val)
plt.title("Imbalance of Motif Reconstruction in Sequencing Pipeline - cumulative")
plt.show()
    

consensus = ["99.74", "60.51", "33.45", "11.45"]
counter = 0 
for i in total_motif_counts:
    mean_val = np.mean(i)
    plt.bar(motifs_label, i)
    plt.xlabel("Motifs")
    plt.ylabel("Errors Per Motif in Sequencing Pipeline")
    plt.axhline(mean_val)
    plt.title(f"Imbalance of Motif Reconstruction in Sequencing for Decoding consensus {consensus[counter]}")
    plt.show()

    counter += 1
# Included missing values - wonder what happens when you throw the missing values away
