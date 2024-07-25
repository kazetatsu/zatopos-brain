import numpy as np
import serial

SOUND_DEPTH = 64
CH_NUM = 6
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
        d = 4

        x = np.ndarray((CH_NUM, SOUND_DEPTH), dtype=np.int16)

        while True:
            s = self.readline().decode()
            if s[:5] == "time:":
                break

        data = self.readline().decode().split('.')
        for i in range(SOUND_DEPTH):
            for ch in range(CH_NUM):
                sounds = data[i].split(',')
                try:
                    x[ch, i] = int(sounds[ch], 16)
                except ValueError:
                    print("stop in i={}, ch={}".format(i, ch))
                    return np.zeros((CH_NUM, SOUND_DEPTH), dtype=np.int16)

        return x
