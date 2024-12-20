
import torch
import torch.nn as nn
import torch.optim as optim
from crnn import CNN_BiGRU_Classifier
import math
from tqdm import tqdm
import numpy as np
from training_data import data_preproc, load_pre_data
from sklearn.model_selection import train_test_split
from greedy_decoder import GreedyCTCDecoder, beam_search_decoder
from utils import get_actual_transcript, get_model_savepath, get_motifs_identified
import torchaudio
import datetime

# Tensorboard
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter()

X,y = data_preproc(chop_reads=1)
print(f"Number of samples: {len(X)}")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
torch.set_default_device(device)
print(f"Running on {device}")

labels_int = np.arange(14).tolist()
labels = [f"{i}" for i in labels_int] # Tokens to be fed into greedy decoder
greedy_decoder = GreedyCTCDecoder(labels=labels)

model_save_path = get_model_savepath()
model_save_iterations = 200

# Model Parameters
input_size = 1  # Number of input channels
hidden_size = 128
num_layers = 4
output_size = 14  # Number of output classes
dropout_rate = 0.2

saved_model = True

# Model Definition
model = CNN_BiGRU_Classifier(input_size, hidden_size, num_layers, output_size, dropout_rate)

if saved_model:
    model_path = "models/model.pth"

    checkpoint = torch.load(model_path)
    model.load_state_dict(checkpoint['model_state_dict'])

model = model.to(device)

optimizer = optim.Adam(model.parameters(), lr=0.0001)
ctc_loss = nn.CTCLoss(zero_infinity=True)

presaved = False

"""
if presaved:
    X, y = load_pre_data()
else:
    X,y = data_preproc()
"""
    
# Creating Train, Test, Validation sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1) 

torch.autograd.set_detect_anomaly(True)

n_classes = 14
step_sequence = 100
window_overlap = 50
length_per_sample = 150
model_output_split_size = 1

epochs = 2

"""
# Add over epochs
for epoch in range(epochs):

    #################### Training Loop #################
    print(f"Epoch {epoch}")
    model.train()
    for i in tqdm(range(len(X_train))):

        training_sequence, target_sequence = X_train[i].to(device), torch.tensor(y_train[i]).to(device)

        input_lengths = torch.tensor(X_train[i].shape[0])
        target_lengths = torch.tensor(len(target_sequence))

        # Zero out the gradients
        optimizer.zero_grad()
        

        try:        
            
            # Give the model the input in chunks based on the model_output_split_size flag
            if model_output_split_size > 1:
                model_output_timestep = torch.zeros([input_lengths, output_size]).to(device)
                stepper_size = (input_lengths + model_output_split_size - 1) // model_output_split_size  # Adjust stepper_size to cover all elements

                for j in range(0, input_lengths, stepper_size):
                    end_index = min(j + stepper_size, len(target_sequence))
                    
                    # Get the model output for the current chunk
                    model_output_chunk = model(training_sequence[j:end_index])
                    
                    # Ensure the sizes match before assignment
                    model_output_timestep[j:end_index] = model_output_chunk
                        
            else:
                model_output_timestep = model(training_sequence) # Getting model output

            loss = ctc_loss(model_output_timestep, target_sequence, input_lengths, target_lengths)
            
            loss.backward()
            # Update the weights
            optimizer.step()

        except Exception as e:
            print(f"Error at {i}")
            print(e)
            model_output_split_size += 1
            continue

        
        if i % 100 == 0:
            print(f"\nEpoch {epoch} Batch {i}")
            print(f"Loss {loss.item()}")
            greedy_result = greedy_decoder(model_output_timestep)
            greedy_transcript = " ".join(greedy_result)
            actual_transcript = get_actual_transcript(target_sequence)
            motif_err = torchaudio.functional.edit_distance(actual_transcript, greedy_result) / len(actual_transcript)

            motifs_identifed = get_motifs_identified(actual_transcript, greedy_transcript)

            print(f"Transcript: {greedy_transcript}")
            print(f"Actual Transcript: {actual_transcript}")
            print(f"Motif Error Rate: {motif_err}")
            print(f"Motifs Identified: {motifs_identifed}")

            writer.add_scalar("Loss/train", loss, epoch)
            writer.add_scalar("Err/Train", motif_err, epoch)
        
        # Saving model weights
        if i % model_save_iterations == 0:
            torch.save({
            'epoch': epoch,
            'batch':i,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
            }, model_save_path)

    ################## Validation Loop ####################
    
    model.eval()
    val_loss = 0.0
    distances_arr = []
    motifs_identifed_arr = []
    with torch.no_grad():
        for i in tqdm(range(len(X_val))):

            validation_sequence, target_sequence = torch.tensor(X_val[i]).to(device), torch.tensor(y_val[i]).to(device)

            model_output_timestep = model(validation_sequence) # Getting model output

            input_lengths = torch.tensor(X_val[i].shape[0])
            target_lengths = torch.tensor(len(target_sequence))

            loss = ctc_loss(model_output_timestep, target_sequence, input_lengths, target_lengths)

            greedy_result = greedy_decoder(model_output_timestep)
            greedy_transcript = " ".join(greedy_result)
            actual_transcript = get_actual_transcript(target_sequence)
            
            motif_err = torchaudio.functional.edit_distance(actual_transcript, greedy_result) / len(actual_transcript)
            distances_arr.append(motif_err)

            motifs_identifed = get_motifs_identified(actual_transcript, greedy_transcript)
            motifs_identifed_arr.append(motifs_identifed)

            val_loss += loss.item()

    val_loss /= len(X_val)
    val_accuracy = np.mean(distances_arr)
    motifs_identifed = np.mean(motifs_identifed_arr)
    print(f"Epoch {epoch}, Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.4f}, Motifs Identified: {motifs_identifed:.4f}")
    writer.add_scalar("Loss/validation", val_loss, epoch)

"""
    


# Test Loop
model.eval()
test_loss = 0.0
distances_arr = []
motifs_identifed_arr = []
with torch.no_grad():
    for i in tqdm(range(len(X_test))):

        test_sequence, target_sequence = torch.tensor(X_test[i]).to(device), torch.tensor(y_test[i]).to(device)

        model_output_timestep = model(test_sequence) # Getting model output

        input_lengths = torch.tensor(X_test[i].shape[0])
        target_lengths = torch.tensor(len(target_sequence))

        loss = ctc_loss(model_output_timestep, target_sequence, input_lengths, target_lengths)
        test_loss += loss.item()

        greedy_result = greedy_decoder(model_output_timestep)
        greedy_transcript = " ".join(greedy_result)
        actual_transcript = get_actual_transcript(target_sequence)


        motif_err = torchaudio.functional.edit_distance(actual_transcript, greedy_transcript) / len(actual_transcript)
        distances_arr.append(motif_err)

        motifs_identifed = get_motifs_identified(actual_transcript, greedy_transcript)
        motifs_identifed_arr.append(motifs_identifed)

        if i % 100 == 0:
            print(f"Transcript: {greedy_transcript}")
            print(f"Actual Transcript: {actual_transcript}")
            print(f"Motif Error Rate: {motif_err}")
            print(f"Motifs Identified: {motifs_identifed}")


test_loss /= len(X_test)
test_accuracy = np.mean(distances_arr)
motifs_identifed = np.mean(motifs_identifed_arr)
print(f"Test Loss: {test_loss:.4f}, Test Edit Distance: {test_accuracy:.4f}, Motifs Identified: {motifs_identifed:.4f}")
