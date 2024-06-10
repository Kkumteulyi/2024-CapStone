from PIL import Image
import torchvision.transforms as transforms
import torch
import numpy as np

# 이미지 불러오기
image_path = "plum1.jpg"
image = Image.open(image_path)

# 이미지 전처리
transform = transforms.Compose([
    transforms.Resize((416, 416)),  # 모델의 입력 크기로 리사이즈
    transforms.ToTensor(),  # 텐서로 변환
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 정규화
])

image_tensor = transform(image)  # 텐서 변환
image_tensor = image_tensor.unsqueeze(0)  # 배치 차원 추가

# 텐서를 바이트 값으로 변환하여 바이트 파일로 저장
tensor_bytes = image_tensor.numpy().tobytes()  # 텐서를 numpy 배열로 변환 후 바이트로 변환

# 바이트 파일 저장
with open("tensor_values.bytes", "wb") as f:
    f.write(tensor_bytes)

# 바이트 파일을 읽어 텐서로 변환
with open("tensor_values.bytes", "rb") as f:
    tensor_bytes = f.read()

# 바이트 데이터를 numpy 배열로 변환
tensor_array = np.frombuffer(tensor_bytes, dtype=np.float32)
tensor_array = tensor_array.reshape((1, 3, 416, 416))  # 원래 텐서의 형태로 변환

# numpy 배열을 텐서로 변환
reconstructed_tensor = torch.tensor(tensor_array)

# 정규화 복원
inv_transform = transforms.Normalize(
    mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
    std=[1/0.229, 1/0.224, 1/0.225]
)

reconstructed_tensor = inv_transform(reconstructed_tensor[0])

# 텐서를 이미지로 변환
reconstructed_image = transforms.ToPILImage()(reconstructed_tensor)

# 이미지 저장
reconstructed_image.save("reconstructed_image.jpg")
