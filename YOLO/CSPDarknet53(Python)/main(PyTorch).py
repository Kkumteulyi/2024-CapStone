import torch
import torch.nn as nn

class BasicBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.leaky_relu = nn.LeakyReLU(0.1)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

    def forward(self, x):
        out = self.leaky_relu(self.bn1(self.conv1(x)))
        out = self.leaky_relu(self.bn2(self.conv2(out)))
        return out

class CSPBlock(nn.Module):
    def __init__(self, in_channels, out_channels, num_blocks):
        super(CSPBlock, self).__init__()
        self.split_channels = out_channels // 2
        self.conv1 = nn.Conv2d(in_channels, self.split_channels, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn1 = nn.BatchNorm2d(self.split_channels)
        self.blocks = nn.Sequential(
            *[BasicBlock(self.split_channels, self.split_channels) for _ in range(num_blocks)]
        )
        self.conv2 = nn.Conv2d(self.split_channels * 2, out_channels, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.leaky_relu = nn.LeakyReLU(0.1)

    def forward(self, x):
        x1 = self.leaky_relu(self.bn1(self.conv1(x)))
        x2 = x
        out = torch.cat((self.blocks(x1), x2), dim=1)
        out = self.leaky_relu(self.bn2(self.conv2(out)))
        return out

class CSPDarknet53(nn.Module):
    def __init__(self):
        super(CSPDarknet53, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(32)
        self.leaky_relu = nn.LeakyReLU(0.1)
        self.layer1 = self._make_layer(32, 64, 1)
        self.layer2 = self._make_layer(64, 128, 2)
        self.layer3 = self._make_layer(128, 256, 8)
        self.layer4 = self._make_layer(256, 512, 8)
        self.layer5 = self._make_layer(512, 1024, 4)

    def _make_layer(self, in_channels, out_channels, num_blocks):
        layers = [
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.1)
        ]
        layers.append(CSPBlock(out_channels, out_channels, num_blocks))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.leaky_relu(self.bn1(self.conv1(x)))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.layer5(x)
        return x

# 모델 생성 및 테스트
model = CSPDarknet53()
x = torch.randn(1, 3, 416, 416)  # 임의의 입력 데이터
output = model(x)
print(output.shape)
