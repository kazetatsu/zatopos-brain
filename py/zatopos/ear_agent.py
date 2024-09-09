import sys
import numpy as np
import os
import ctypes
import subprocess

from .sound import *

LIBZATOPOS_PATH = os.path.join(sys.prefix, "lib", "libzatopos.so")

class EarAgent:
    def __init__(self, bus_no, dev_addr):
        self.libzatopos = ctypes.cdll.LoadLibrary(LIBZATOPOS_PATH)

        self.c_agent = ctypes.c_void_p(self.libzatopos.ear_agent_malloc())

        ret = self.libzatopos.ear_agent_init(self.c_agent, bus_no, dev_addr)

        if ret != 0:
            self.libzatopos.ear_agent_delete(self.c_agent)
            raise ValueError()

        self.sound_buf = (ctypes.c_ushort * SOUND_BUF_LEN)()
        self.libzatopos.ear_agent_copy_sound.argtypes = (ctypes.c_void_p, (ctypes.c_ushort * SOUND_BUF_LEN))


    def __del__(self):
        self.libzatopos.ear_agent_delete(self.c_agent)


    def read_sound(self, dtype=np.int16) -> np.ndarray:
        ret = self.libzatopos.ear_agent_receive(self.c_agent)
        if ret != 0:
            raise ValueError("%x" % ret)

        self.libzatopos.ear_agent_copy_sound(self.c_agent, self.sound_buf)
        sound = np.ctypeslib.as_array(self.sound_buf).astype(dtype).reshape((SOUND_DEPTH, NUM_MIC_CHS)).T

        return sound


def get_ear_agent() -> EarAgent:
    ret_lsusb = subprocess.run("lsusb | grep kazetatsu", shell=True, stdout=subprocess.PIPE)
    if ret_lsusb.stdout is None:
        raise Exception("subprocess error")

    ss = ret_lsusb.stdout.decode().splitlines()

    if len(ss) == 0:
        raise Exception("no device")

    cs = ss[0].split(' ')
    bus_no = int(cs[1])
    dev_addr = int(cs[3][0:3])
    return EarAgent(bus_no, dev_addr)
