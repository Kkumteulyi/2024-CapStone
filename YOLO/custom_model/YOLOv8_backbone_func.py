import numpy as np

# Basic layers



def conv2d(input, filters, bias, stride=2, padding=1):
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

def silu(input):
    return input * (1 / (1 + np.exp(-input)))

def batch_norm(input, gamma, beta, eps=1e-5):
    batch_size, num_channels, height, width = input.shape
    
    mean = np.mean(input, axis=(0, 2, 3), keepdims=True)
    variance = np.var(input, axis=(0, 2, 3), keepdims=True)
    
    input_normalized = (input - mean) / np.sqrt(variance + eps)
    
    output = gamma.reshape(1, num_channels, 1, 1) * input_normalized + beta.reshape(1, num_channels, 1, 1)
    
    return output

def conv_layer(input, filters, bias, gamma, beta, stride=2, padding=1):
    out = conv2d(input, filters, bias, stride, padding)
    out = batch_norm(out, gamma, beta)
    out = silu(out)
    return out

def residual_block(input, filters1, bias1, filters2, bias2, gamma, beta):
    out = conv2d(input, filters1, bias1, stride=1, padding=1)
    out = batch_norm(out, gamma, beta)
    out = silu(out)
    
    out = conv2d(out, filters2, bias2, stride=1, padding=1)
    out = batch_norm(out, gamma, beta)
    
    out += input
    out = silu(out)
    
    return out

def c2f_layer(input, num_blocks, filters1, bias1, filters2, bias2, gamma1, beta1, gamma2, beta2):
    channels = input.shape[1]
    split_channels = channels // 2
    
    x1 = input[:, :split_channels, :, :]
    x2 = input[:, split_channels:, :, :]
    
    for _ in range(num_blocks):
        x1 = residual_block(x1, filters1, bias1, filters2, bias2, gamma1, beta1)
    
    out = np.concatenate((x1, x2), axis=1)
    
    out = batch_norm(out, gamma2, beta2)  
    
    return out

# For SPPF

def max_pooling(input, size, stride, padding):
    batch_size, channels, height, width = input.shape
    output_height = (height - size + 2 * padding) // stride + 1
    output_width = (width - size + 2 * padding) // stride + 1
    
    output = np.zeros((batch_size, channels, output_height, output_width))
    
    padded_input = np.pad(input, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode='constant')
    
    for i in range(0, output_height):
        for j in range(0, output_width):
            output[:, :, i, j] = np.max(
                padded_input[:, :, i*stride:i*stride+size, j*stride:j*stride+size], axis=(2, 3)
            )
    return output

def sppf_layer(input, conv1_filters, conv1_bias, conv2_filters, conv2_bias):
    # 첫 번째 Conv 레이어
    conv1 = conv2d(input, conv1_filters, conv1_bias, stride=1, padding=1)
    
    # 세 번의 MaxPooling 레이어
    pool1 = max_pooling(conv1, size=5, stride=1, padding=2)
    pool2 = max_pooling(conv1, size=9, stride=1, padding=4)
    pool3 = max_pooling(conv1, size=13, stride=1, padding=6)
    
    # Concat
    concat = np.concatenate([conv1, pool1, pool2, pool3], axis=1)
    
    # 마지막 Conv 레이어
    output = conv2d(concat, conv2_filters, conv2_bias, stride=1, padding=1)
    
    return output

# For Detect
def detect_layer(input, bbox_filters1, bbox_bias1, bbox_filters2, bbox_bias2, cls_filters1, cls_bias1, cls_filters2, cls_bias2):
    # BBox Regression Branch
    bbox = conv_layer(input, bbox_filters1, bbox_bias1, np.ones(bbox_filters1.shape[0]), np.zeros(bbox_filters1.shape[0]), stride=1)
    bbox = conv_layer(bbox, bbox_filters2, bbox_bias2, np.ones(bbox_filters2.shape[0]), np.zeros(bbox_filters2.shape[0]), stride=1)
    bbox_output = conv2d(bbox, np.random.randn(bbox_filters2.shape[0], bbox_filters2.shape[0], 1, 1), np.zeros(bbox_filters2.shape[0]))

    # Classification Branch
    cls = conv_layer(input, cls_filters1, cls_bias1, np.ones(cls_filters1.shape[0]), np.zeros(cls_filters1.shape[0]), stride=1)
    cls = conv_layer(cls, cls_filters2, cls_bias2, np.ones(cls_filters2.shape[0]), np.zeros(cls_filters2.shape[0]), stride=1)
    cls_output = conv2d(cls, np.random.randn(cls_filters2.shape[0], cls_filters2.shape[0], 1, 1), np.zeros(cls_filters2.shape[0]))

    # Concatenate or merge as needed
    return bbox_output, cls_output


def decode_bbox(bbox_output, grid_size, stride, confidence_threshold=0.5):
    # bbox_output shape: (batch_size, num_boxes, 5, grid_size)
    batch_size, num_boxes, num_params, _ = bbox_output.shape  # Adjusted to four dimensions

    # Extract parameters
    cx = bbox_output[:, :, 0, :]  # Center X
    cy = bbox_output[:, :, 1, :]  # Center Y
    w = bbox_output[:, :, 2, :]    # Width
    h = bbox_output[:, :, 3, :]    # Height
    confidence = bbox_output[:, :, 4, :]  # Confidence score

    # Initialize lists for storing coordinates
    left = []
    top = []
    right = []
    bottom = []

    # Loop through each bounding box
    for b in range(batch_size):
        for i in range(num_boxes):
            # Check if the confidence score is above the threshold
            if confidence[b, i].max() >= confidence_threshold:  # Check the maximum confidence for the box
                # Convert to absolute coordinates
                cx_pixel = cx[b, i] * stride
                cy_pixel = cy[b, i] * stride
                w_pixel = w[b, i] * stride
                h_pixel = h[b, i] * stride

                # Calculate corners of the bounding boxes
                left_x = cx_pixel - (w_pixel / 2)
                top_y = cy_pixel - (h_pixel / 2)
                right_x = cx_pixel + (w_pixel / 2)
                bottom_y = cy_pixel + (h_pixel / 2)

                # Append to lists
                left.append(left_x)
                top.append(top_y)
                right.append(right_x)
                bottom.append(bottom_y)

    return np.array(left), np.array(top), np.array(right), np.array(bottom)

# --------------------- Layer test --------------------------

# 0번 레이어: Conv
input = np.random.randn(1, 3, 240, 320)  # (batch_size, channels, height, width)
filters = np.random.randn(16, 3, 3, 3)
bias = np.random.randn(16)
gamma = np.random.randn(16)
beta = np.random.randn(16)
output_0 = conv_layer(input, filters, bias, gamma, beta, stride=2, padding=1)
print(f"output 0 shape : {output_0.shape}")

# 1번 레이어: Conv
filters = np.random.randn(32, 16, 3, 3)
bias = np.random.randn(32)
gamma = np.random.randn(32)
beta = np.random.randn(32)
output_1 = conv_layer(output_0, filters, bias, gamma, beta, stride=2, padding=1)
print(f"output 1 shape : {output_1.shape}")

# 2번 레이어: C2f
filters1 = np.random.randn(16, 16, 3, 3)  
bias1 = np.random.randn(16)
filters2 = np.random.randn(16, 16, 3, 3)
bias2 = np.random.randn(16)
gamma1 = np.random.randn(16)  
beta1 = np.random.randn(16)
gamma2 = np.random.randn(32)  
beta2 = np.random.randn(32)
output_2 = c2f_layer(output_1, num_blocks=1, filters1=filters1, bias1=bias1, filters2=filters2, bias2=bias2, gamma1=gamma1, beta1=beta1, gamma2=gamma2, beta2=beta2)
print(f"output 2 shape : {output_2.shape}")

# 3번 레이어: Conv
filters = np.random.randn(64, 32, 3, 3)
bias = np.random.randn(64)
gamma = np.random.randn(64)
beta = np.random.randn(64)
output_3 = conv_layer(output_2, filters, bias, gamma, beta, stride=2, padding=1)
print(f"output 3 shape : {output_3.shape}")

# 4번 레이어: C2f
filters1 = np.random.randn(32, 32, 3, 3)
bias1 = np.random.randn(32)
filters2 = np.random.randn(32, 32, 3, 3)
bias2 = np.random.randn(32)
gamma1 = np.random.randn(32)
beta1 = np.random.randn(32)
gamma2 = np.random.randn(64)
beta2 = np.random.randn(64)
output_4 = c2f_layer(output_3, num_blocks=1, filters1=filters1, bias1=bias1, filters2=filters2, bias2=bias2, gamma1=gamma1, beta1=beta1, gamma2=gamma2, beta2=beta2)
print(f"output 4 shape : {output_4.shape}")

# 5번 레이어: Conv
filters = np.random.randn(128, 64, 3, 3)
bias = np.random.randn(128)
gamma = np.random.randn(128)
beta = np.random.randn(128)
output_5 = conv_layer(output_4, filters, bias, gamma, beta, stride=2, padding=1)
print(f"output 5 shape : {output_5.shape}")

# 6번 레이어: C2f
filters1 = np.random.randn(64, 64, 3, 3)
bias1 = np.random.randn(64)
filters2 = np.random.randn(64, 64, 3, 3)
bias2 = np.random.randn(64)
gamma1 = np.random.randn(64)
beta1 = np.random.randn(64)
gamma2 = np.random.randn(128)
beta2 = np.random.randn(128)
output_6 = c2f_layer(output_5, num_blocks=1, filters1=filters1, bias1=bias1, filters2=filters2, bias2=bias2, gamma1=gamma1, beta1=beta1, gamma2=gamma2, beta2=beta2)
print(f"output 6 shape : {output_6.shape}")

# 7번 레이어: Conv
filters = np.random.randn(256, 128, 3, 3)
bias = np.random.randn(256)
gamma = np.random.randn(256)
beta = np.random.randn(256)
output_7 = conv_layer(output_6, filters, bias, gamma, beta, stride=2, padding=1)
print(f"output 7 shape : {output_7.shape}")

# 8번 레이어: C2f
filters1 = np.random.randn(128, 128, 3, 3)
bias1 = np.random.randn(128)
filters2 = np.random.randn(128, 128, 3, 3)
bias2 = np.random.randn(128)
gamma1 = np.random.randn(128)
beta1 = np.random.randn(128)
gamma2 = np.random.randn(256)
beta2 = np.random.randn(256)
output_8 = c2f_layer(output_7, num_blocks=1, filters1=filters1, bias1=bias1, filters2=filters2, bias2=bias2, gamma1=gamma1, beta1=beta1, gamma2=gamma2, beta2=beta2)
print(f"output 8 shape : {output_8.shape}")

# 9번 레이어: SPPF
conv1_filters = np.random.randn(256, 256, 3, 3)  # 입력 채널: 256, 출력 채널: 256
conv1_bias = np.random.randn(256)
conv2_filters = np.random.randn(256, 1024, 3, 3)  # 입력 채널: 1024, 출력 채널: 256 (concat 후 채널 수)
conv2_bias = np.random.randn(256)

output_9 = sppf_layer(output_8, conv1_filters, conv1_bias, conv2_filters, conv2_bias)
print(f"output 9 shape : {output_9.shape}")

# # 10번 레이어: Detect
# bbox_filters1 = np.random.randn(256, 256, 3, 3)
# bbox_bias1 = np.random.randn(256)
# bbox_filters2 = np.random.randn(256, 256, 3, 3)
# bbox_bias2 = np.random.randn(256)

# cls_filters1 = np.random.randn(256, 256, 3, 3)
# cls_bias1 = np.random.randn(256)
# cls_filters2 = np.random.randn(256, 256, 3, 3)
# cls_bias2 = np.random.randn(256)

# bbox_output_10, cls_output_10 = detect_layer(output_9, bbox_filters1, bbox_bias1, bbox_filters2, bbox_bias2, cls_filters1, cls_bias1, cls_filters2, cls_bias2)

# print(f"BBox output shape : {bbox_output_10.shape}")
# print(f"Cls output shape : {cls_output_10.shape}")


# bbox_output = bbox_output_10  
# grid_size = 6  
# stride = 32    
# left, top, right, bottom = decode_bbox(bbox_output, grid_size, stride)

# print("Left coordinates: ", left)
# print("Top coordinates: ", top)
# print("Right coordinates: ", right)
# print("Bottom coordinates: ", bottom)
