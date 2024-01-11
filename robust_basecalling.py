
import numpy as np
import ast
import pandas as pd
import matplotlib.pyplot as plt
# Checking which motifs are most robust to basecalling error

def read_payloads_from_file(filename):

    df = pd.read_csv(filename, sep="\t")
    # Getting purely the payload columns
    payloads = df.drop(['ONT_Barcode', 'HW_Address'], axis=1)
    payloads_arr = payloads.to_numpy()
    payloads_arr = np.array([[ast.literal_eval(j) for j in i] for i in payloads_arr])
    payloads_arr = payloads_arr.reshape(8*1280*4) # Flattening completely into a motif array
    return payloads_arr

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
motifs_label = ['1', '2', '3', '4', '5', '6', '7', '8']

for i in range(4):
    wrong_motif_count = np.zeros(8)
    for j in range(40960):
        if not encoded_motifs[i,j] == decoded_motifs[i,j]:
            original_motif = encoded_motifs[i,j] # This is after masking though, we are blind to the actual motifs, just showing whether differences exist
            wrong_motif_count[original_motif-1] += 1
            total_motif_count[original_motif-1] += 1
    wrong_motif_counts.append(wrong_motif_count)

mean_val = np.mean(total_motif_count)
plt.bar(motifs_label, total_motif_count)
plt.xlabel("Motifs")
plt.ylabel("Errors Per Motif in Sequencing Pipeline")
plt.axhline(mean_val)
plt.title("Imbalance of Motif Reconstruction in Sequencing Pipeline - on average")
plt.show()
    