import sys
import numpy as np
import serial
import os
import ctypes
import subprocess

from .sound import *

DATA_BYTE = 4 # how many bytes per one value

LIBZATOPOS_PATH = os.path.join(sys.prefix, "lib", "libzatopos.so")

class WorkerAgentBase:
    def __init__(self):
        pass
    def read_sound(self, dtype=np.int16) -> np.ndarray:
        pass


class WorkerAgentSerial(WorkerAgentBase, serial.Serial):
    def __init__(self, port, baudrate=115200):
        WorkerAgentBase.__init__(self)
        serial.Serial.__init__(self, port=port, baudrate=baudrate)


    def read_sound(self, length:int, dtype=np.int16) -> np.ndarray:
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

        return x.astype(np.int16)


class WorkerAgentUSB(WorkerAgentBase):
    def __init__(self, bus_no, dev_addr):
        WorkerAgentBase.__init__(self)
        self.libzatopos = ctypes.cdll.LoadLibrary(LIBZATOPOS_PATH)

        self.c_agent = ctypes.c_void_p(self.libzatopos.worker_agent_malloc())

        ret = self.libzatopos.worker_agent_init(self.c_agent, bus_no, dev_addr)

        if ret != 0:
            self.libzatopos.worker_agent_delete(self.c_agent)
            raise ValueError()

        self.sound_buf = (ctypes.c_ushort * SOUND_BUF_LEN)()
        self.libzatopos.worker_agent_copy_sound.argtypes = (ctypes.c_void_p, (ctypes.c_ushort * SOUND_BUF_LEN))


    def __del__(self):
        self.libzatopos.worker_agent_delete(self.c_agent)


    def read_sound(self, dtype=np.int16) -> np.ndarray:
        ret = self.libzatopos.worker_agent_receive(self.c_agent)
        if ret != 0:
            raise ValueError("%x" % ret)

        self.libzatopos.worker_agent_copy_sound(self.c_agent, self.sound_buf)
        sound = np.ctypeslib.as_array(self.sound_buf).astype(dtype).reshape((SOUND_DEPTH, NUM_MIC_CHS)).T

        return sound


def get_worker_agent() -> WorkerAgentBase:
    ret_lsusb = subprocess.run("lsusb | grep kazetatsu", shell=True, stdout=subprocess.PIPE)
    if ret_lsusb.stdout is None:
        raise Exception("subprocess error")

    ss = ret_lsusb.stdout.decode().splitlines()

    if len(ss) == 0:
        raise Exception("no device")

    cs = ss[0].split(' ')
    bus_no = int(cs[1])
    dev_addr = int(cs[3][0:3])
    return WorkerAgentUSB(bus_no, dev_addr)
