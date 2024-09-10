from ctypes import *

import numpy as np

from .sound import *
from ._load_lib import load_libzatopos
from ._ctypes_numpy_convert import _np2c_2darr, _np2c_3darr

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
            c_freq = \
                np.fft.fftfreq(n=SOUND_DEPTH, d=SOUND_SAMPLING_TIME)\
                .ctypes.data_as(POINTER(c_float))
            c_freq_len = c_int(SOUND_DEPTH)
        else:
            c_freq = freq.ctypes.data_as(POINTER(c_float))
            c_freq_len = c_int(freq.shape[0])
        self.libzatopos.locator_set_frequency(
            self.c_locator,
            c_freq, c_freq_len
        )


    def __del__(self):
        self.libzatopos.locator_delete(self.c_locator)


    def locate(self, signal_spaces:np.ndarray) -> np.ndarray:
        shape = signal_spaces.shape
        assert len(shape) == 3
        assert shape[1] == NUM_MIC_CHS
        assert shape[2] == NUM_MIC_CHS
        ss_type = np.ctypeslib.ndpointer(dtype=np.uintp, ndim=2)
        c_signal_spaces_re = _np2c_3darr(signal_spaces.real.astype(np.float32))
        c_signal_spaces_im = _np2c_3darr(signal_spaces.imag.astype(np.float32))
        result = np.zeros(shape=(self.resolution[0], self.resolution[1]), dtype=np.float32)
        c_result = _np2c_2darr(result) # c_result and result share memory
        # ↓で止まる
        self.libzatopos.locator_locate(self.c_locator, c_signal_spaces_re, c_signal_spaces_im, c_result)
        return result
