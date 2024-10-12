# SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

from ctypes import *
import subprocess

import numpy as np

from ._load_lib import load_libzatopos


EAR_NUM_MICS = 6
EAR_WINDOW_LEN = 64
EAR_BUFFER_LEN = EAR_NUM_MICS * EAR_WINDOW_LEN
EAR_SAMPLING_RATE = 2000 # [Hz]
EAR_WINDOW_TIME = EAR_WINDOW_LEN / EAR_SAMPLING_RATE


class EarAgent:
    def __init__(self, bus_no, dev_addr):
        self.libzatopos = load_libzatopos()

        self.c_agent = self.libzatopos.ear_agent_malloc()

        ret = self.libzatopos.ear_agent_init(self.c_agent, bus_no, dev_addr)

        if ret != 0:
            self.libzatopos.ear_agent_delete(self.c_agent)
            raise ValueError()

        self.sound_buf = np.ndarray(shape=(EAR_BUFFER_LEN,), dtype=np.uint16)
        self.c_sound_buf = c_void_p(self.sound_buf.__array_interface__["data"][0])


    def __del__(self):
        self.libzatopos.ear_agent_delete(self.c_agent)


    def read_sound(self, dtype=np.int16) -> np.ndarray:
        ret = self.libzatopos.ear_agent_receive(self.c_agent)
        if ret != 0:
            raise ValueError("%x" % ret)

        self.libzatopos.ear_agent_copy_sound(self.c_agent, self.c_sound_buf)
        sound = self.sound_buf.reshape((EAR_WINDOW_LEN, EAR_NUM_MICS)).T

        return sound.astype(dtype)


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
