from ctypes import *

import numpy as np

from ._ear_agent import EAR_WINDOW_LEN, EAR_WINDOW_TIME, EAR_NUM_MICS
from ._load_lib import load_libzatopos

class Locator:
    def __init__(self,
        resolution:tuple[int,int]=(8,8),
        distance:tuple[float,float]=(10.0,10.0),
        freq_filter:np.ndarray=None
    ):
        self.libzatopos = load_libzatopos()

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

        freq = np.fft.fftfreq(n=EAR_WINDOW_LEN, d=(EAR_WINDOW_LEN/EAR_WINDOW_TIME)).astype(np.float32)
        if freq_filter is not None:
            freq = freq[freq_filter]
        else:
            freq = freq[1:np.uint16(np.ceil(EAR_WINDOW_LEN/2))]
        self.libzatopos.locator_set_frequency(
            self.c_locator,
            c_void_p(freq.__array_interface__["data"][0]),
            c_int(freq.shape[0])
        )


    def __del__(self):
        self.libzatopos.locator_delete(self.c_locator)


    def locate(self, signal_spaces:np.ndarray) -> np.ndarray:
        shape = signal_spaces.shape
        assert len(shape) == 3
        assert shape[1] == EAR_NUM_MICS
        assert shape[2] == EAR_NUM_MICS
        assert signal_spaces.dtype == np.complex64

        result = np.zeros(shape=(self.resolution[0], self.resolution[1]), dtype=np.float32)

        # BUG: ここでresultがnanまたはinfの行列になっちゃう
        self.libzatopos.locator_locate(
            self.c_locator,
            c_void_p(signal_spaces.__array_interface__["data"][0]),
            c_void_p(result.__array_interface__["data"][0])
        )
        return result
