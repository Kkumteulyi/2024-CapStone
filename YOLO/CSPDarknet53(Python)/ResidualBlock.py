def residual_block(input, filters1, bias1, filters2, bias2, gamma, beta):
    # 첫 번째 합성곱
    out = conv2d(input, filters1, bias1, stride=1, padding=1)
    out = batch_norm(out, gamma, beta)
    out = leaky_relu(out)
    
    # 두 번째 합성곱
    out = conv2d(out, filters2, bias2, stride=1, padding=1)
    out = batch_norm(out, gamma, beta)
    
    # 입력과 출력 더하기
    out += input
    
    # 활성화 함수 적용
    out = leaky_relu(out)
    
    return out

# 예제 입력
input = np.random.randn(1, 16, 30, 30)
filters1 = np.random.randn(16, 16, 3, 3)
bias1 = np.random.randn(16)
filters2 = np.random.randn(16, 16, 3, 3)
bias2 = np.random.randn(16)
gamma = np.ones(16)
beta = np.zeros(16)

output = residual_block(input, filters1, bias1, filters2, bias2, gamma, beta)
print(output.shape)  # 예상 출력: (1, 16, 30, 30)
