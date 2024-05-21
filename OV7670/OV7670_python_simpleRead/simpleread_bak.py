import serial
import numpy as np
from bmp import BMP
import time

COMMAND = ['*', 'R', 'D', 'Y', '*']
WIDTH = 320
HEIGHT = 240

def read(input_stream):
    c = input_stream.read(1)
    if c == b'':
        return -1
    return ord(c)

def is_image_start(input_stream, index):
    if index < len(COMMAND):
        val = read(input_stream)
        if val == -1:
            return False
        if COMMAND[index] == chr(val):
            return is_image_start(input_stream, index + 1)
        return False
    return True

class SimpleRead:
    def __init__(self, port_name='COM2'):
        self.port_name = port_name
        self.serial_port = serial.Serial(port_name, 1000000, timeout=1)
        self.array1 = np.zeros((HEIGHT, WIDTH), dtype=np.uint32)
        self.array2 = np.zeros((WIDTH, HEIGHT), dtype=np.uint32)
        self.bmp = BMP()
        self.run()

    def run(self):
        image_count = 0
        try:
            while True:
                print("Looking for image")
                while not is_image_start(self.serial_port, 0):
                    pass
                print(f"Found image: {image_count}")

                for y in range(HEIGHT):
                    for x in range(WIDTH):
                        i = -1
                        retries = 0
                        while i == -1 and retries < 10:
                            i = read(self.serial_port)
                            retries += 1
                            if i == -1:
                                time.sleep(0.1)  # wait for 100 ms before retrying
                        if i == -1:
                            raise Exception("Serial port read error after retries")
                        self.array1[y][x] = (i & 0xFF) << 16 | (i & 0xFF) << 8 | (i & 0xFF)

                for y in range(HEIGHT):
                    for x in range(WIDTH):
                        self.array2[x][y] = self.array1[y][x]

                self.bmp.saveBMP(f"c:/out/{image_count}.bmp", self.array2)
                print(f"Saved image: {image_count}")
                image_count += 1
                
                # Reset the serial port input buffer
                self.serial_port.reset_input_buffer()

        except Exception as e:
            print(e)
            self.serial_port.close()
            return

if __name__ == "__main__":
    SimpleRead()
