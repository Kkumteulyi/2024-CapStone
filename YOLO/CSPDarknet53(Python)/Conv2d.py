import numpy as np

def conv2d(input, filters, bias, stride=1, padding=0):
    # 입력 데이터의 크기
    batch_size, in_channels, in_height, in_width = input.shape
    out_channels, _, filter_height, filter_width = filters.shape
    
    # 패딩 적용
    if padding > 0:
        input = np.pad(input, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode='constant')
    
    # 출력 데이터 크기 계산
    out_height = (in_height - filter_height + 2 * padding) // stride + 1
    out_width = (in_width - filter_width + 2 * padding) // stride + 1
    
    # 출력 데이터 초기화
    output = np.zeros((batch_size, out_channels, out_height, out_width))
    
    for b in range(batch_size):
        for c in range(out_channels):
            for i in range(0, out_height):
                for j in range(0, out_width):
                    for k in range(in_channels):
                        output[b, c, i, j] += np.sum(
                            input[b, k, i*stride:i*stride+filter_height, j*stride:j*stride+filter_width] * filters[c, k]
                        )
                    output[b, c, i, j] += bias[c]
    return output

# 예제 입력
input = np.random.randn(1, 3, 32, 32)
filters = np.random.randn(16, 3, 3, 3)
bias = np.random.randn(16)

output = conv2d(input, filters, bias)
print(output.shape)  # 예상 출력: (1, 16, 30, 30)
