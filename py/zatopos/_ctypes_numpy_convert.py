from ctypes import *
import numpy as np

def _np2c_2darr(src:np.ndarray) -> c_void_p:
    assert len(src.shape) == 2

    first_addr = src.__array_interface__["data"][0]
    addrs = (np.arange(src.shape[0]) * src.strides[0] + first_addr).astype(np.uintp)

    # Return address of first element of "addrs"
    return c_void_p(addrs.__array_interface__["data"][0])


def _np2c_3darr(src:np.ndarray) -> c_void_p:
    assert len(src.shape) == 3

    addrs = np.array(
        [_np2c_2darr(src[i]).value
         for i in range(src.shape[0])],
        dtype=np.uintp
    )

    return c_void_p(addrs.__array_interface__["data"][0])
