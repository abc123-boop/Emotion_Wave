import numpy as np
import torch
from torch.utils.data import Dataset

# Load dataset
features = np.load("audio_features.npy", allow_pickle=True)
labels = np.load("audio_labels.npy", allow_pickle=True)

print("Features Data Type:", features.dtype, "| First Feature:", features[0])
print("Labels Data Type:", labels.dtype, "| First Label:", labels[0])

# Print unique labels for debugging
unique_labels = np.unique(labels)
print("🔍 Unique Labels in Dataset:", unique_labels)

class EmotionDataset(Dataset):
    def __init__(self, feature_path="audio_features.npy", label_path="audio_labels.npy"):
        self.features = np.load(feature_path, allow_pickle=True).astype(np.float32)
        self.labels = np.load(label_path, allow_pickle=True)

        # Define the label map
        label_map = {
    "neutral": 0, "happy": 1, "sad": 2, "angry": 3, 
    "fearful": 4, "disgust": 5, "surprised": 6, "calm": 7
}


        # Convert labels
        self.labels = np.array([label_map.get(label, -1) for label in self.labels], dtype=np.int64)

        # Check for unmapped labels
        if -1 in self.labels:
            print("❌ Unmapped labels detected!")
            unmapped_labels = [label for label in unique_labels if label not in label_map]
            print("⚠️ Unmapped Labels:", unmapped_labels)
            raise ValueError("❌ Some labels are not mapped correctly. Check the label names in `label_map`.")

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return torch.tensor(self.features[idx], dtype=torch.float32), torch.tensor(self.labels[idx], dtype=torch.long)

# Load dataset
dataset = EmotionDataset()
print(f"✅ Dataset Loaded: {len(dataset)} samples")
