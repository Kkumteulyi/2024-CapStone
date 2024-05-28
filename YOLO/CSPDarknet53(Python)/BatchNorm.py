def batch_norm(input, gamma, beta, eps=1e-5):
    batch_size, num_channels, height, width = input.shape
    
    # 채널별 평균과 분산 계산
    mean = np.mean(input, axis=(0, 2, 3), keepdims=True)
    variance = np.var(input, axis=(0, 2, 3), keepdims=True)
    
    # 정규화
    input_normalized = (input - mean) / np.sqrt(variance + eps)
    
    # 스케일과 시프트 적용
    output = gamma.reshape(1, num_channels, 1, 1) * input_normalized + beta.reshape(1, num_channels, 1, 1)
    
    return output

# 예제 입력
input = np.random.randn(1, 16, 30, 30)
gamma = np.ones(16)
beta = np.zeros(16)

output = batch_norm(input, gamma, beta)
print(output.shape)  # 예상 출력: (1, 16, 30, 30)
