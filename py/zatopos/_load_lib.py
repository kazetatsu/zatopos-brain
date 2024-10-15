# SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

from ctypes import *
import sys
import os

def load_libzatopos() -> CDLL:
    path = os.path.join(sys.prefix, "lib", "libzatopos.so")

    libzatopos = cdll.LoadLibrary(path)

    # ear_driver_t* ear_driver_malloc();
    libzatopos.ear_driver_malloc.argtypes = ()
    libzatopos.ear_driver_malloc.restype  = c_void_p
    # unsigned int ear_driver_init(ear_driver_t *driver, unsigned char bus_no, unsigned char dev_addr);
    libzatopos.ear_driver_init.argtypes = (c_void_p, c_ubyte, c_ubyte)
    libzatopos.ear_driver_init.restype  = c_uint
    # void ear_driver_delete(ear_driver_t *driver);
    libzatopos.ear_driver_delete.argtypes = (c_void_p,)
    libzatopos.ear_driver_delete.restype  = None
    # unsigned int ear_driver_receive(ear_driver_t *driver, unsigned char* sound_buf, unsigned char num_windows);
    libzatopos.ear_driver_receive.argtypes = (c_void_p, c_void_p, c_ubyte)
    libzatopos.ear_driver_receive.restype  = c_uint

    # musical_t* musical_malloc(void)
    libzatopos.musical_malloc.argtypes = ()
    libzatopos.musical_malloc.restype  = c_void_p
    # unsigned int musical_init(musical_t* music)
    libzatopos.musical_init.argtypes = (c_void_p,)
    libzatopos.musical_init.restype  = c_uint
    # void musical_delete(musical_t* music)
    libzatopos.musical_delete.argtypes = (c_void_p,)
    libzatopos.musical_delete.restype  = None
    # unsigned int musical_set_frequency(musical_t* music, float* freq, int len)
    libzatopos.musical_set_frequency.argtypes = (c_void_p, c_void_p, c_int)
    libzatopos.musical_set_frequency.restype  = c_uint
    # unsigned int musical_set_resolution(musical_t* music, int x, int y)
    libzatopos.musical_set_resolution.argtypes = (c_void_p, c_int, c_int)
    libzatopos.musical_set_resolution.restype  = c_uint
    # unsigned int musical_set_distance(musical_t* music, float x, float y)
    libzatopos.musical_set_distance.argtypes = (c_void_p, c_float, c_float)
    libzatopos.musical_set_distance.restype  = c_uint
    # unsigned int musical_search(musical_t* music, float *E, float *result)
    libzatopos.musical_search.argtypes = (c_void_p, c_void_p, c_void_p)
    libzatopos.musical_search.restype  = c_uint

    return libzatopos
