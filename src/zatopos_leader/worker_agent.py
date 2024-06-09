import numpy as np
import serial

SOUND_DEPTH = 64
CH_NUM = 1
DATA_BYTE = 4 # how many bytes per one value

class WorkerAgentBase:
    def __init__(self):
        pass
    def read_sound(self) -> np.ndarray:
        pass


class WorkerAgentSerial(WorkerAgentBase, serial.Serial):
    def __init__(self, port, baudrate=115200):
        WorkerAgentBase.__init__(self)
        serial.Serial.__init__(self, port=port, baudrate=baudrate)


    def read_sound(self) -> np.ndarray:
        n = CH_NUM * SOUND_DEPTH
        d = DATA_BYTE * 2

        x = np.ndarray((n,), dtype=np.int16)

        self.write("r".encode())
        data = self.readline().decode()
        for i in range(n):
            x[i] = int(data[d*i : d*i+d], 16)

        return x.reshape((CH_NUM, SOUND_DEPTH))
