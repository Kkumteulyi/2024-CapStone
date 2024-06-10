# 바이트 파일을 읽어 16진수 값으로 변환하여 출력
with open("tensor_values.bytes", "rb") as f:
    tensor_bytes = f.read()

# 16진수로 변환
hex_values = tensor_bytes.hex()

# 텍스트 파일에 저장
with open("tensor_values_hex.txt", "w") as f:
    for i in range(0, len(hex_values), 2):
        f.write(hex_values[i:i+2] + " ")
    f.write("\n")

# ----------------------------------------------------------------
# Float32 to Hex value
# import struct

# # 읽을 파일 이름과 저장할 파일 이름
# input_file = "float_values.txt"
# output_file = "hex_values.txt"

# # float32 값을 hex로 변환하는 함수
# def float_to_hex(float_value):
#     byte_array = struct.pack('f', float_value)
#     return ''.join(format(byte, '02x') for byte in byte_array)

# # 입력 파일을 읽어서 각 줄의 float32 값을 읽고, hex로 변환하여 출력 파일에 저장
# with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
#     for line in f_in:
#         # 문자열을 float32로 변환
#         float_value = float(line.strip())
        
#         # float32 값을 hex로 변환
#         hex_value = float_to_hex(float_value)
        
#         # hex 값을 출력 파일에 저장
#         f_out.write(hex_value + "\n")

# print("Hex values saved to", output_file)
