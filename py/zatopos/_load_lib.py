# SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

from ctypes import *
import sys
import os

def load_libzatopos() -> CDLL:
    path = os.path.join(sys.prefix, "lib", "libzatopos.so")

    libzatopos = cdll.LoadLibrary(path)

    # ear_agent_t* ear_agent_malloc();
    libzatopos.ear_agent_malloc.argtypes = ()
    libzatopos.ear_agent_malloc.restype  = c_void_p
    # unsigned int ear_agent_init(ear_agent_t *agent, unsigned char bus_no, unsigned char dev_addr);
    libzatopos.ear_agent_init.argtypes = (c_void_p, c_ubyte, c_ubyte)
    libzatopos.ear_agent_init.restype  = c_uint
    # void ear_agent_delete(ear_agent_t *agent);
    libzatopos.ear_agent_delete.argtypes = (c_void_p,)
    libzatopos.ear_agent_delete.restype  = None
    # unsigned int ear_agent_receive(ear_agent_t *agent, unsigned char* sound_buf, unsigned char num_windows);
    libzatopos.ear_agent_receive.argtypes = (c_void_p, c_void_p, c_ubyte)
    libzatopos.ear_agent_receive.restype  = c_uint

    # locator_t* locator_malloc(void)
    libzatopos.locator_malloc.argtypes = ()
    libzatopos.locator_malloc.restype  = c_void_p
    # unsigned int locator_init(locator_t* locator)
    libzatopos.locator_init.argtypes = (c_void_p,)
    libzatopos.locator_init.restype  = c_uint
    # void locator_delete(locator_t* locator)
    libzatopos.locator_delete.argtypes = (c_void_p,)
    libzatopos.locator_delete.restype  = None
    # unsigned int locator_set_frequency(locator_t* locator, float* freq, int len)
    libzatopos.locator_set_frequency.argtypes = (c_void_p, c_void_p, c_int)
    libzatopos.locator_set_frequency.restype  = c_uint
    # unsigned int locator_set_resolution(locator_t* locator, int x, int y)
    libzatopos.locator_set_resolution.argtypes = (c_void_p, c_int, c_int)
    libzatopos.locator_set_resolution.restype  = c_uint
    # unsigned int locator_set_distance(locator_t* locator, float x, float y)
    libzatopos.locator_set_distance.argtypes = (c_void_p, c_float, c_float)
    libzatopos.locator_set_distance.restype  = c_uint
    # unsigned int locator_locate(locator_t* locator, float *E, float *result)
    libzatopos.locator_locate.argtypes = (c_void_p, c_void_p, c_void_p)
    libzatopos.locator_locate.restype  = c_uint

    return libzatopos
