from ctypes import *
import sys
import os

from .sound import *

def load_libzatopos() -> CDLL:
    path = os.path.join(sys.prefix, "lib", "libzatopos.so")

    libzatopos = cdll.LoadLibrary(path)

    libzatopos.ear_agent_malloc.argtypes = ()
    libzatopos.ear_agent_malloc.restype  = c_void_p

    libzatopos.ear_agent_init.argtypes = (c_void_p, c_ubyte, c_ubyte)
    libzatopos.ear_agent_init.restype  = c_int

    libzatopos.ear_agent_delete.argtypes = (c_void_p,)
    libzatopos.ear_agent_delete.restype  = None

    libzatopos.ear_agent_receive.argtypes = (c_void_p,)
    libzatopos.ear_agent_receive.restype  = c_uint

    libzatopos.ear_agent_copy_sound.argtypes = (c_void_p, (c_ushort * (NUM_MIC_CHS * SOUND_DEPTH)))
    libzatopos.ear_agent_copy_sound.restype  = None

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
    libzatopos.locator_set_frequency.restype  = c_uint
    # unsigned int locator_set_resolution(locator_t* locator, int x, int y)
    libzatopos.locator_set_resolution.argtypes = (c_void_p, c_int, c_int)
    libzatopos.locator_set_resolution.restype  = c_uint
    # unsigned int locator_set_distance(locator_t* locator, float x, float y)
    libzatopos.locator_set_distance.argtypes = (c_void_p, c_float, c_float)
    libzatopos.locator_set_distance.restype  = c_uint
    # unsigned int locator_locate(locator_t* locator, float ***E_re, float ***E_im, float **result)
    libzatopos.locator_locate.restype  = c_uint

    return libzatopos
