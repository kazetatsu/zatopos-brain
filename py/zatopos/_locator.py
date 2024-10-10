from ctypes import *

import numpy as np

from .sound import *
from ._load_lib import load_libzatopos

class Locator:
    def __init__(self,
        resolution:tuple[int,int]=(8,8),
        distance:tuple[float,float]=(10.0,10.0),
        freq:np.ndarray=None,
        libzatopos:CDLL=None
    ):
        if libzatopos is None:
            self.libzatopos = load_libzatopos()
        else:
            self.libzatopos = libzatopos

        self.c_locator:c_void_p = self.libzatopos.locator_malloc()
        self.libzatopos.locator_init(self.c_locator)

        self.resolution = resolution
        self.libzatopos.locator_set_resolution(
            self.c_locator,
            c_int(resolution[0]), c_int(resolution[1])
        )

        self.libzatopos.locator_set_distance(
            self.c_locator,
            c_float(distance[0]), c_float(distance[1])
        )

        if freq is None:
            _freq = np.fft.fftfreq(n=SOUND_DEPTH, d=SOUND_SAMPLING_TIME).astype(np.float32)
            c_freq_len = c_int(SOUND_DEPTH)
        else:
            _freq = freq.astype(np.float32)
            c_freq_len = c_int(freq.shape[0])
        self.libzatopos.locator_set_frequency(
            self.c_locator,
            c_void_p(_freq.__array_interface__["data"][0]), c_freq_len
        )


    def __del__(self):
        self.libzatopos.locator_delete(self.c_locator)


    def locate(self, signal_spaces:np.ndarray) -> np.ndarray:
        shape = signal_spaces.shape
        assert len(shape) == 3
        assert shape[1] == NUM_MIC_CHS
        assert shape[2] == NUM_MIC_CHS
        assert signal_spaces.dtype == np.complex64

        result = np.zeros(shape=(self.resolution[0], self.resolution[1]), dtype=np.float32)

        self.libzatopos.locator_locate(
            self.c_locator,
            c_void_p(signal_spaces.__array_interface__["data"][0]),
            c_void_p(result.__array_interface__["data"][0])
        )
        return result
