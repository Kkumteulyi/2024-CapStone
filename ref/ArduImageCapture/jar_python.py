import serial
import time

class SerialReaderException(Exception):
    pass

class JSerialCommSerialReader:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            if self.ser.is_open:
                print(f"Opened port {self.port} successfully.")
            else:
                raise SerialReaderException(f"Failed to open port {self.port}.")
        except serial.SerialException as e:
            raise SerialReaderException(f"Error opening port {self.port}: {e}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Closed port {self.port}.")

    def read(self):
        if self.ser and self.ser.is_open:
            try:
                line = self.ser.readline().decode('utf-8').rstrip()
                print(f"Read from port {self.port}: {line}")
                return line
            except serial.SerialException as e:
                raise SerialReaderException(f"Error reading from port {self.port}: {e}")
        else:
            raise SerialReaderException(f"Port {self.port} is not open.")

    def write(self, data):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(data.encode())
                print(f"Wrote to port {self.port}: {data}")
            except serial.SerialException as e:
                raise SerialReaderException(f"Error writing to port {self.port}: {e}")
        else:
            raise SerialReaderException(f"Port {self.port} is not open.")

if __name__ == "__main__":
    reader = JSerialCommSerialReader('/dev/ttyUSB0', baudrate=9600, timeout=1)
    try:
        reader.open()
        time.sleep(2)  # Wait for the serial connection to initialize
        reader.write("Hello, Arduino!")
        time.sleep(1)
        response = reader.read()
        print(f"Response: {response}")
    except SerialReaderException as e:
        print(e)
    finally:
        reader.close()