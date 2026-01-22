import torch
from torchvision import datasets, models
from torch import nn, optim
from torch.utils.data import DataLoader
from transforms import get_train_transforms, get_test_transforms
import os

# Paths
DATA_DIR = "../data"
MODEL_SAVE_PATH = "../models/mask_detector.pth"

# Training parameters
BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 0.001

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device)

    # Load dataset
    train_dataset = datasets.ImageFolder(
        root=DATA_DIR,
        transform=get_train_transforms()
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    # Load pretrained model
    model = models.mobilenet_v2(pretrained=True)

    # Freeze backbone
    for param in model.parameters():
        param.requires_grad = False

    # Replace classifier
    model.classifier[1] = nn.Linear(model.last_channel, 2)

    model = model.to(device)

    # Loss & optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=LEARNING_RATE)

    # Training loop
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {running_loss / len(train_loader)}")

    # Save model
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print("Model saved to", MODEL_SAVE_PATH)

if __name__ == "__main__":
    main()
