import serial  # pip install pyserial
import binascii  # pip install binascii

idx = 0
distance = 0

try:
    # Change Serial('COM Port to your environment')
    ser = serial.Serial('COM5', 115200)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

while True:
    if ser.readable():
        s = ser.read(1)  # Reading 1 byte at a time
        hex_string = binascii.hexlify(s).decode('utf-8')

        if idx == 4 or idx == 5:
            # Append incoming hex values and convert to decimal
            if idx == 4:
                distance = int(hex_string, 16) << 8  # Shift left by 8 bits for the high byte
            elif idx == 5:
                distance += int(hex_string, 16)  # Add the low byte value
                print(f"Distance: {distance} mm")  # Print the distance

        if idx == 6 and hex_string != '00':
            print("WARNING: Out of range!")
        # Index increment
        idx += 1
        
        if hex_string == 'fa':
            # Reset packet on end signal
            idx = 0
            distance = 0
            print("\n")