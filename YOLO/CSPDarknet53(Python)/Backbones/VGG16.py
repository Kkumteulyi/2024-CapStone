import numpy as np

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

def conv2d(input, filters, bias, stride=1, padding=1):
    batch_size, in_channels, in_height, in_width = input.shape
    out_channels, _, filter_height, filter_width = filters.shape

    if padding > 0:
        input = np.pad(input, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode='constant')

    out_height = (in_height - filter_height + 2 * padding) // stride + 1
    out_width = (in_width - filter_width + 2 * padding) // stride + 1

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

def max_pooling(input, size=2, stride=2):
    batch_size, channels, in_height, in_width = input.shape
    out_height = (in_height - size) // stride + 1
    out_width = (in_width - size) // stride + 1

    output = np.zeros((batch_size, channels, out_height, out_width))

    for b in range(batch_size):
        for c in range(channels):
            for i in range(0, out_height):
                for j in range(0, out_width):
                    output[b, c, i, j] = np.max(
                        input[b, c, i*stride:i*stride+size, j*stride:j*stride+size]
                    )
    return output

def flatten(input):
    return input.reshape(input.shape[0], -1)

def fully_connected(input, weights, bias):
    return np.dot(input, weights) + bias

# 예제 입력
input = np.random.randn(1, 3, 224, 224)

# 간단한 VGG16 레이어 구성
conv1_filters = np.random.randn(64, 3, 3, 3)
conv1_bias = np.random.randn(64)

# 첫 번째 합성곱 레이어
output = conv2d(input, conv1_filters, conv1_bias)
output = relu(output)

# 첫 번째 풀링 레이어
output = max_pooling(output)

# 두 번째 합성곱 레이어
conv2_filters = np.random.randn(128, 64, 3, 3)
conv2_bias = np.random.randn(128)
output = conv2d(output, conv2_filters, conv2_bias)
output = relu(output)

# 두 번째 풀링 레이어
output = max_pooling(output)

# 플래튼 및 완전 연결 레이어
output = flatten(output)
fc_weights = np.random.randn(output.shape[1], 1000)
fc_bias = np.random.randn(1000)
output = fully_connected(output, fc_weights, fc_bias)
output = softmax(output)

print(output.shape)  # 예상 출력: (1, 1000)
