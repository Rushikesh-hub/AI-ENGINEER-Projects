import torch
from torchvision import models
from torchvision.models import MobileNet_V2_Weights

MODEL_PATH = "../models/mask_detector.pth"
TORCHSCRIPT_PATH = "../models/mask_detector_torchscript.pt"

def main():
    model = models.mobilenet_v2(weights = None)
    model.classifier[1] = torch.nn.Linear(model.last_channel,2)
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()

    example_input = torch.randn(1,3,224,224)

    traced_model = torch.jit.trace(model, example_input)
    traced_model.save(TORCHSCRIPT_PATH)

    print("TorchScript model saved to:", TORCHSCRIPT_PATH)

if __name__ == "__main__":
    main()