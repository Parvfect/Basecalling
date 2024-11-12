

import torch
import torch.nn as nn
import numpy as np
from collections import defaultdict

class GreedyCTCDecoder(nn.Module):

    def __init__(self, labels, blank=0):
        super().__init__()
        self.labels=labels
        self.blank = blank

    def forward(self, emission:torch.Tensor):
        """Given a sequence emission over labels, get the best path"""
        
        indices = torch.argmax(emission, dim=-1)
        indices = torch.unique_consecutive(indices, dim=-1)
        indices = [i for i in indices if i != self.blank]
        joined = " ".join([self.labels[i] for i in indices])
        return joined.replace("|", " ").strip()
    

def beam_search_decoder(probabilities, beam_width=2, blank_index=0):
    """
    Beam search decoder for CTC output.
    
    Args:
    probabilities (np.array): Shape (time_steps, num_classes)
    beam_width (int): Number of beams to keep at each step
    blank_index (int): Index of the blank token
    
    Returns:
    list: Decoded sequence of characters
    """

    # detaching the probabilities from the GPU
    probabilities = probabilities.cpu().detach().numpy()
    # make a copy of the probabilities
    probabilities = np.array(probabilities)

    T, S = probabilities.shape  # T: time steps, S: number of classes
    
    # Initialize the beam
    beam = [([], 0)]  # (prefix, log_probability)
    
    for t in range(T):
        new_beam = defaultdict(float)
        
        for prefix, log_p in beam:
            for s in range(S):
                new_prefix = prefix + [s]
                new_log_p = log_p + np.log(probabilities[t, s])
                
                # If this label is different from the last one and not blank, add it
                if s != blank_index and (not prefix or s != prefix[-1]):
                    new_beam[tuple(new_prefix)] = max(new_beam[tuple(new_prefix)], new_log_p)
                
                # If this label is blank or the same as the last one, don't add it
                if s == blank_index or (prefix and s == prefix[-1]):
                    new_beam[tuple(prefix)] = max(new_beam[tuple(prefix)], new_log_p)
        
        # Keep only the top beam_width beams
        beam = sorted(new_beam.items(), key=lambda x: x[1], reverse=True)[:beam_width]
        beam = [(list(k), v) for k, v in beam]
    
    print(beam)
    # Return the best path
    return beam