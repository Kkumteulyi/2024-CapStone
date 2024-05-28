def csp_block(input, num_blocks, filters1, bias1, filters2, bias2, gamma, beta):
    channels = input.shape[1]
    split_channels = channels // 2
    
    # 입력을 두 부분으로 나누기
    x1 = input[:, :split_channels, :, :]
    x2 = input[:, split_channels:, :, :]
    
    # 잔차 블록 적용
    for _ in range(num_blocks):
        x1 = residual_block(x1, filters1, bias1, filters2, bias2, gamma, beta)
    
    # 두 부분 결합
    out = np.concatenate((x1, x2), axis=1)
    
    return out

# 예제 입력
input = np.random.randn(1, 16, 30, 30)
filters1 = np.random.randn(8, 8, 3, 3)
bias1 = np.random.randn(8)
filters2 = np.random.randn(8, 8, 3, 3)
bias2 = np.random.randn(8)
gamma = np.ones(8)
beta = np.zeros(8)

output = csp_block(input, num_blocks=1, filters1=filters1, bias1=bias1, filters2=filters2, bias2=bias2, gamma=gamma, beta=beta)
print(output.shape)  # 예상 출력: (1, 16, 30, 30)
