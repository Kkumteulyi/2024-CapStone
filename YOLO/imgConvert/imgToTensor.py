import torchvision.transforms as transforms
import torch
from PIL import Image

# Load the image
image_path = "./img.png"
image = Image.open(image_path)

# Define the transformation
transform = transforms.Compose([
    transforms.ToTensor()
])

# Convert the image to a tensor
image_tensor = transform(image)

print(image_tensor.shape)

tf = transforms.ToPILImage()(image_tensor)

tf.save("output.png")
