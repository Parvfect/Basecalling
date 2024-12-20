
import torch
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import normalize
from tqdm import tqdm
import math
import pickle


def load_training_data(dataset_path=None):

    if dataset_path is None:
        dataset_path = r"C:\Users\Parv\Doc\HelixWorks\Basecalling\cycle_dataset\short_read_dataset.pkl"

    dataset  = pd.read_pickle(dataset_path)

    X = dataset['squiggle'].to_numpy().tolist()

    y = dataset['Spacer_Sequence'].to_numpy()

    return X, y
        

def data_preproc(dataset_path=None, chop_reads=1):
    
    step_sequence = 100
    window_overlap = 50
    length_per_sample = 150

    X, y = load_training_data(dataset_path=dataset_path)

    if chop_reads < 1:
      y = y[:int(len(X)*chop_reads)]
      X = X[:int(len(X)*chop_reads)]

    # So we split and norm it
    sequences_dataset = []
    for i in tqdm(X):
        j = normalize([i]).flatten()

        sequence_length = len(j)
            
        n_samples = math.ceil(sequence_length//step_sequence) # Since we send the last one even if it is small as can be

        ptr = 0
        counter = 0
        sequences = torch.zeros([n_samples, 1, length_per_sample])
        while ptr <= sequence_length:
            
            try:
                if ptr + length_per_sample > sequence_length:
                    break
                    sequence_chop = j[ptr:ptr+length_per_sample]
                    
                    sequence_chop = j[ptr:-1] # For when the window has crossed the end
                    pad = np.zeros(length_per_sample - (sequence_length-ptr) + 1)
                    sequence_chop = np.concatenate((sequence_chop, pad)).tolist()
                else:
                    sequence_chop = j[ptr:ptr+length_per_sample]
                    
                sequence_chop = torch.tensor(sequence_chop, dtype=torch.float32).view(1, len(sequence_chop))

                sequences[counter] = sequence_chop
            except IndexError:
                print("Index problem")
                
            
            ptr += step_sequence
            counter+=1
        
        sequences_dataset.append(sequences)
        
    """
    with open('X.pkl', 'wb') as f:
        pickle.dump(sequences_dataset, f)

    with open('y.pkl', 'w') as f:
        pickle.dump(y, f)
    """
         
    return sequences_dataset, y


def load_pre_data():

    f = open('X.pkl', 'rb')
    X = pickle.load(f)
    f.close()

    dataset  = pd.read_pickle(r"C:\Users\Parv\Doc\HelixWorks\Basecalling\code\synth_dataset.pkl")

    y = dataset['Motifs'].to_numpy()

    y_ = []
    
    for i in range(len(y)):
        new_seq = ""
        old_seq = y[i]
        tmp_arr = []
        for c in old_seq:
            tmp_arr.append(int(int(c) + 1))
            new_seq += f"{int(c)+1}"
        y_.append(tmp_arr)
    
    return X, y_



