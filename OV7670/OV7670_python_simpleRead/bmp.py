import numpy as np

class BMP:
    def readBMP(self, filename):
        with open(filename, 'rb') as f:
            header = f.read(54)
            width = int.from_bytes(header[18:22], byteorder='little')
            height = int.from_bytes(header[22:26], byteorder='little')
            array = np.zeros((height, width), dtype=np.uint32)

            for y in range(height):
                for x in range(width):
                    b, g, r = f.read(3)
                    array[y][x] = (r << 16) | (g << 8) | b

        return array

    def saveBMP(self, filename, array):
        height, width = array.shape
        with open(filename, 'wb') as f:
            f.write(self.createBMPHeader(width, height))
            for y in range(height):
                for x in range(width):
                    pixel = array[y][x]
                    f.write(bytes([pixel & 0xFF, (pixel >> 8) & 0xFF, (pixel >> 16) & 0xFF]))

    def createBMPHeader(self, width, height):
        file_size = 54 + 3 * width * height
        header = bytearray(54)
        header[0:2] = b'BM'
        header[2:6] = file_size.to_bytes(4, byteorder='little')
        header[10:14] = (54).to_bytes(4, byteorder='little')
        header[14:18] = (40).to_bytes(4, byteorder='little')
        header[18:22] = width.to_bytes(4, byteorder='little')
        header[22:26] = height.to_bytes(4, byteorder='little')
        header[26:28] = (1).to_bytes(2, byteorder='little')
        header[28:30] = (24).to_bytes(2, byteorder='little')
        return header
