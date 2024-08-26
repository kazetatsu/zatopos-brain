import numpy as np
import serial
import os
import ctypes

NUM_MIC_CHS = 6
SOUND_DEPTH = 64
SOUND_BUF_LEN = NUM_MIC_CHS * SOUND_DEPTH
DATA_BYTE = 4 # how many bytes per one value

LIBZATOPOS_PATH = os.path.dirname(__file__) + "../../c/build/libzatopos.so"

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

        x = np.zeros(shape=(NUM_MIC_CHS, length), dtype=np.int16)

        i = 0
        loop = 0
        while i < length and loop < 1.5 * length:
            sounds = self.readline().decode().strip().split(',')

            error_msg = None

            if len(sounds) != NUM_MIC_CHS:
                error_msg = "too many/few words @ i={}".format(i)
            else:
                for ch in range(NUM_MIC_CHS):
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

class WorkerAgentUSB(WorkerAgentBase):
    def __init__(self, bus_no, dev_addr):
        WorkerAgentBase.__init__(self)
        self.libzatopos = ctypes.cdll.LoadLibrary(LIBZATOPOS_PATH)

        self.receiver = self.libzatopos.receiver_malloc()
        self.receiver = ctypes.c_void_p(self.receiver)

        ret = self.libzatopos.receiver_init(self.receiver, bus_no, dev_addr)

        if ret != 0:
            self.libzatopos.receiver_delete(self.receiver)
            raise ValueError()

        self.sound = (ctypes.c_ushort * SOUND_BUF_LEN)()
        self.libzatopos.receiver_get_data.argtypes = (ctypes.c_void_p, (ctypes.c_ushort * SOUND_BUF_LEN))


    def read_sound(self, length:int) -> np.ndarray:
        ret = self.libzatopos.receiver_receive(self.receiver)
        if ret != 0:
            self.libzatopos.receiver_delete(self.receiver)
            raise ValueError()

        self.libzatopos.receiver_get_data(self.receiver, self.sound)
        self.sound = np.ctypeslib.as_array(self.sound).reshape((NUM_MIC_CHS, SOUND_DEPTH))
