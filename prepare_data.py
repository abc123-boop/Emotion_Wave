import os
import librosa
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader

# Define emotion labels in RAVDESS (corresponds to file naming convention)
emotion_map = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised"
}

# Path to dataset
dataset_path = r"C:\Users\bhava\.cache\kagglehub\datasets\uwrfkaggler\ravdess-emotional-speech-audio\versions\1"

# Function to load and process audio files
def load_audio_files():
    audio_data = []
    labels = []

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                label_code = file.split("-")[2]  # Extract emotion label
                if label_code in emotion_map:
                    y, sr = librosa.load(file_path, sr=16000)
                    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)  # Extract MFCC features
                    mfccs = np.mean(mfccs.T, axis=0)  # Take mean across time axis
                    audio_data.append(mfccs)
                    labels.append(emotion_map[label_code])

    return np.array(audio_data), np.array(labels)

# Load dataset
X, y = load_audio_files()
print(f"Loaded {len(X)} samples with labels: {set(y)}")


# Save extracted features and labels
np.save("audio_features.npy", X)  # Save extracted audio features
np.save("audio_labels.npy", y)    # Save corresponding emotion labels

print("✅ Features and labels saved as 'audio_features.npy' and 'audio_labels.npy'")

import librosa
import numpy as np

def extract_features(audio_path):
    """Extracts MFCC features from an audio file with correct shape for the model."""
    try:
        audio_data, sr = librosa.load(audio_path, sr=16000)  
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=40)  

        # Compute mean along time axis (reduces shape from (40, time_steps) to (40,))
        mfccs = np.mean(mfccs, axis=1)

        return mfccs
    
    except Exception as e:
        print(f"❌ Error extracting features: {e}")
        return None
