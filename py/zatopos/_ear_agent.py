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
    def __init__(self, bus_no:int, dev_addr:int):
        self.libzatopos = load_libzatopos()

        self.c_agent = self.libzatopos.ear_agent_malloc()

        ret = self.libzatopos.ear_agent_init(
            self.c_agent,
            c_ubyte(bus_no), c_ubyte(dev_addr)
        )

        if ret != 0:
            self.libzatopos.ear_agent_delete(self.c_agent)
            raise ValueError()


    def __del__(self):
        self.libzatopos.ear_agent_delete(self.c_agent)


    def receive(self, sounds_buf:np.ndarray) -> None:
        assert sounds_buf.nbytes % (EAR_WINDOW_LEN * EAR_NUM_MICS * 2) == 0

        num_windows = int(sounds_buf.nbytes / (EAR_WINDOW_LEN * EAR_NUM_MICS * 2))

        ret = self.libzatopos.ear_agent_receive(
            self.c_agent,
            c_void_p(sounds_buf.__array_interface__["data"][0]), c_ubyte(num_windows)
        )

        if ret != 0:
            raise ValueError("%x" % ret)
        return


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
