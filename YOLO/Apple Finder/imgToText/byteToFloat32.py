import struct

# 바이트 파일을 읽기 모드로 열기
with open("tensor_values.bytes", "rb") as f:
    # 파일에서 모든 바이트 배열 읽기
    byte_data = f.read()

# 바이트 배열을 float32 값으로 변환하여 리스트에 저장
float_values = []
index = 0
while index + 4 <= len(byte_data):  # 4바이트씩 끊어서 읽기
    float_value = struct.unpack('f', byte_data[index:index+4])[0]
    float_values.append(float_value)
    index += 4

# 읽은 float32 값을 새로운 파일에 저장
with open("float_values.txt", "w") as f:
    for value in float_values:
        f.write(str(value) + "\n")

print("Float values saved to float_values.txt")
