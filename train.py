import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import StepLR
from sklearn.metrics import accuracy_score
from dataset import EmotionDataset
from model import EmotionModel  # Import the model
import itertools

# Define device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load dataset
dataset = EmotionDataset()
train_loader = DataLoader(dataset, batch_size=16, shuffle=True)

# Hyperparameter search space
param_grid = {
    "batch_size": [16, 32, 64],
    "learning_rate": [1e-3, 1e-4, 1e-5],
    "optimizer": ["AdamW", "SGD", "RMSprop"],
    "step_size": [2, 3, 5],  # LR scheduler step sizes
    "gamma": [0.5, 0.7, 0.9],  # LR scheduler gamma values
}

# Generate all combinations of hyperparameters
best_acc = 0
best_params = {}

for params in itertools.product(*param_grid.values()):
    batch_size, lr, opt, step_size, gamma = params
    print(f"🔍 Testing: batch_size={batch_size}, lr={lr}, optimizer={opt}, step_size={step_size}, gamma={gamma}")

    # Reload dataset with new batch size
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Create model and move to device
    model = EmotionModel().to(device)

    # Define optimizer dynamically
    if opt == "AdamW":
        optimizer = optim.AdamW(model.parameters(), lr=lr)
    elif opt == "SGD":
        optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.9)
    elif opt == "RMSprop":
        optimizer = optim.RMSprop(model.parameters(), lr=lr)

    # Define loss function and learning rate scheduler
    loss_fn = nn.CrossEntropyLoss()
    scheduler = StepLR(optimizer, step_size=step_size, gamma=gamma)

    # Training Loop
    num_epochs = 5
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for batch in train_loader:
            inputs, labels = batch
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
        
        scheduler.step()  # Update learning rate

    # Evaluate Model
    model.eval()
    predictions, true_labels = [], []

    with torch.no_grad():
        for batch in train_loader:
            inputs, labels = batch
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            preds = torch.argmax(outputs, dim=-1).cpu().numpy()
            labels = labels.cpu().numpy()

            predictions.extend(preds)
            true_labels.extend(labels)

    accuracy = accuracy_score(true_labels, predictions)
    print(f"🔹 Accuracy: {accuracy * 100:.2f}%")

    # Track best model
    if accuracy > best_acc:
        best_acc = accuracy
        best_params = {
            "batch_size": batch_size,
            "learning_rate": lr,
            "optimizer": opt,
            "step_size": step_size,
            "gamma": gamma,
        }
        torch.save(model.state_dict(), "best_emotion_model.pth")
        print("✅ New best model saved!")

# Print best hyperparameters
print(f"\n🎯 Best Hyperparameters: {best_params}")
print(f"🔥 Best Accuracy: {best_acc * 100:.2f}%")
