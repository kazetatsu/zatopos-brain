import numpy as np
import serial

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


    def read_sound(self, length:int) -> np.ndarray:
        d = 4

        x = np.zeros(shape=(CH_NUM, length), dtype=np.int16)

        i = 0
        loop = 0
        while i < length and loop < 1.5 * length:
            sounds = self.readline().decode().strip().split(',')

            error_msg = None

            if len(sounds) != CH_NUM:
                error_msg = "too many/few words @ i={}".format(i)
            else:
                for ch in range(CH_NUM):
                    if len(sounds[ch]) != 3:
                        error_msg = "too many/few letters @ i={} ch={}".format(i,ch)
                        break

                    try:
                        x[ch, i] = int(sounds[ch], 16)
                    except ValueError:
                        error_msg = "data is not integer @ i={} ch={}".format(i, ch)
                        break

                    if x[ch, i] >= 1024 or x[ch, i] < 0:
                        error_msg = "data is too big/small @ i={} ch={}".format(i, ch)
                        break

            if error_msg == None:
                i += 1
            else:
                print(error_msg)
                print(sounds)
            loop += 1

        return x
