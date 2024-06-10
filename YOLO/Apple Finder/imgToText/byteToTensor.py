import numpy as np
import torch

# 바이트 파일을 읽어 텐서로 변환
with open("tensor_values.bytes", "rb") as f:
    tensor_bytes = f.read()

# 바이트 데이터를 numpy 배열로 변환
tensor_array = np.frombuffer(tensor_bytes, dtype=np.float32)
tensor_array = tensor_array.reshape((1, 3, 416, 416))  # 원래 텐서의 형태로 변환

# numpy 배열을 텐서로 변환
reconstructed_tensor = torch.tensor(tensor_array)

# 텐서를 텍스트 파일로 저장
with open("reconstructed_tensor.txt", "w") as f:
    # 텐서 값을 1차원 배열로 변환하여 각 값들을 파일에 저장
    for value in reconstructed_tensor.flatten():
        f.write(f"{value.item()}\n")

print("Tensor saved to reconstructed_tensor.txt")
