import torch
from torchvision import models,transforms
from torchvision.models import MobileNet_V2_Weights
from PIL import Image
import os

MODEL_PATH = "../models/mask_detector.pth"
CLASS_NAMES = ["with_mask","without_mask"]

# Image preprocessing (must match training)

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

def load_model():
    model = models.mobilenet_v2(weights = None)
    model.classifier[1] = torch.nn.Linear(model.last_channel,2)
    model.load_state_dict(torch.load(MODEL_PATH,map_location= "cpu"))
    model.eval()
    return model

def predict(image_path):
    model = load_model()

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0) # add batch dimension

    with torch.no_grad():
        outputs = model(image)
        _,predicted = torch.max(outputs,1)

    return CLASS_NAMES[predicted.item()]

if __name__ == "__main__":
    img_path = input("Enter image path: ")
    prediction = predict(img_path)
    print("Prediction:",prediction)

