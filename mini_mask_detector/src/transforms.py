from torchvision import transforms

def get_train_tranforms():
    return transforms.Compose([
        transforms.Resize((224,224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor()
    ])

def get_test_tranforms():
    return transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor()
    ])
