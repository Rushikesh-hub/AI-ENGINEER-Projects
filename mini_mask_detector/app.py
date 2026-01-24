import streamlit as st
import torch
from torchvision import models, transforms
from torchvision.models import MobileNet_V2_Weights
from PIL import Image
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "mask_detector.pth")

CLASS_NAMES = ["with_mask", "without_mask"]

# Preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

@st.cache_resource
def load_model():
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = torch.nn.Linear(model.last_channel, 2)
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()
    return model

model = load_model()

st.title("😷 Face Mask Detector")
st.write("Upload an image and the AI will tell if the person is wearing a mask.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", width=400)

    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)

    result = CLASS_NAMES[predicted.item()]

    if result == "with_mask":
        st.success("Person is wearing a mask 😷")
    else:
        st.error("Person is NOT wearing a mask ❌")
