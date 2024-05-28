def leaky_relu(input, alpha=0.1):
    return np.where(input > 0, input, input * alpha)

# 예제 입력
input = np.random.randn(1, 16, 30, 30)
output = leaky_relu(input)
print(output.shape)  # 예상 출력: (1, 16, 30, 30)
