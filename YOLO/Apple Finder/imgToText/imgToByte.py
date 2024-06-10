from PIL import Image
import torchvision.transforms as transforms
import torch

# 이미지 불러오기
image_path = "plum1.jpg"
image = Image.open(image_path)

# 이미지 전처리
transform = transforms.Compose([
    transforms.Resize((416, 416)),  # 모델의 입력 크기로 리사이즈
    transforms.ToTensor(),  # 텐서로 변환
    # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 정규화
])

image_tensor = transform(image)  # 텐서 변환
image_tensor = image_tensor.unsqueeze(0)  # 배치 차원 추가

# 텐서를 바이트 값으로 변환하여 텍스트 파일로 저장
tensor_bytes = image_tensor.numpy().tobytes()  # 텐서를 numpy 배열로 변환 후 바이트로 변환

# 텍스트 파일에 저장
with open("tensor_values.bytes", "wb") as f:
    f.write(tensor_bytes)
