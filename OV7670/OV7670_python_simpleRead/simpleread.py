import serial
import numpy as np
import cv2  # Add OpenCV for real-time video display
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

                # Convert array1 to a format suitable for OpenCV
                image = self.array1.astype(np.uint8)
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convert grayscale to BGR

                # Crop the image for stereo vision (left and right 90%)
                left_image = image[:, :int(WIDTH * 0.9)]
                right_image = image[:, int(WIDTH * 0.1):]

                # Display the images
                cv2.imshow('Left Image', left_image)
                cv2.imshow('Right Image', right_image)

                # Check for exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                image_count += 1

                # Reset the serial port input buffer
                self.serial_port.reset_input_buffer()

        except Exception as e:
            print(e)
        finally:
            self.serial_port.close()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    SimpleRead()
