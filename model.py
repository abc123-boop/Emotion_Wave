import torch
import torch.nn as nn

class EmotionModel(nn.Module):
    def __init__(self):
        super(EmotionModel, self).__init__()
        self.fc1 = nn.Linear(40, 128)
        self.bn1 = nn.BatchNorm1d(128)  # ✅ Normalize activations
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)   # ✅ BatchNorm again
        self.fc3 = nn.Linear(64, 8)     # ✅ Ensure 8 output classes

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)   # ✅ Normalize before activation
        x = self.relu(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.fc3(x)   # No activation here (CrossEntropyLoss applies softmax)
        return x
