"""Load the compiled C library with ctypes and declare each function's types."""
import ctypes
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAME = "fastsum.dll" if sys.platform == "win32" else "libfastsum.so"

lib = ctypes.CDLL(os.path.join(ROOT, NAME))

# Without these declarations ctypes assumes every argument and return value is a
# C int, which silently truncates 64-bit numbers and garbles doubles.
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int
lib.sum_range.argtypes = [ctypes.c_int64]
lib.sum_range.restype = ctypes.c_int64
lib.sum_array.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]
lib.sum_array.restype = ctypes.c_double
lib.dot.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]
lib.dot.restype = ctypes.c_double
