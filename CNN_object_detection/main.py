import torch
import torch.nn as nn 
import torch.optim as optim 
import torchvision.models as models 
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

# 데이터셋이 저장된 폴더 경로
data_dir = './dataset/'

# 전처리 설정
transform = transforms.Compose([
    transforms.Resize((640, 480)),  # 이미지 크기 조정
    transforms.ToTensor(),          # 이미지를 Tensor로 변환
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 정규화
])

# ImageFolder를 사용하여 각 분할(train, valid, test) 데이터셋 로드
train_dataset = ImageFolder(root=data_dir + 'train', transform=transform)
valid_dataset = ImageFolder(root=data_dir + 'valid', transform=transform)
test_dataset = ImageFolder(root=data_dir + 'test', transform=transform)

# 데이터 로더 정의
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# 클래스 개수
num_classes = len(train_dataset.classes)

# 데이터셋 사용 예시
for images, labels in train_loader:
    # 이미지와 레이블 사용 예시
    print(images.shape, labels.shape)
    break  # 첫 번째 배치만 확인


class RCNN(nn.Module):
    def __init__(self, num_classes, pretrained=True):
        super(RCNN, self).__init__()
        
        # 사전 훈련된 ResNet-50 모델 로드
        self.resnet = models.resnet50(pretrained=pretrained)
        
        # ResNet의 마지막 fully connected layer를 사용하지 않음
        self.resnet = nn.Sequential(*list(self.resnet.children())[:-2])
        
        # 객체 분류를 위한 fully connected layer
        self.fc_cls = nn.Linear(2048, num_classes)
        
        # bounding box 위치 예측을 위한 fully connected layer
        self.fc_bbox = nn.Linear(2048, 4)
        
    def forward(self, x):
        # 이미지를 ResNet에 통과시켜 특성을 추출
        x = self.resnet(x)
        
        # global average pooling을 통해 공간적 정보를 잃지 않고 특성을 압축
        x = nn.functional.adaptive_avg_pool2d(x, (1, 1))
        
        # 특성을 벡터로 변환
        x = torch.flatten(x, 1)
        
        # 객체 분류 예측
        object_classes = self.fc_cls(x)
        
        # bounding box 위치 예측
        bbox_regression = self.fc_bbox(x)
        
        return object_classes, bbox_regression

# 모델 초기화
model = RCNN(num_classes=20, pretrained=True)

# 손실 함수와 옵티마이저 정의
criterion_cls = nn.CrossEntropyLoss()
criterion_bbox = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 예제 입력 데이터
input_tensor = torch.randn(1, 3, 224, 224)  # 크기 224x224의 RGB 이미지

# 모델 추론
object_classes, bbox_regression = model(input_tensor)

# 손실 계산 (실제 데이터셋이 없으므로 예제용으로 임의의 값 사용)
cls_loss = criterion_cls(object_classes, torch.LongTensor([0]))  # 0번 클래스
bbox_loss = criterion_bbox(bbox_regression, torch.randn(1, 4))  # 임의의 bounding box 예측

# 역전파 및 가중치 업데이트
optimizer.zero_grad()
total_loss = cls_loss + bbox_loss
total_loss.backward()
optimizer.step()

# 모델 저장 (옵션)
torch.save(model.state_dict(), 'rcnn_model.pth')
