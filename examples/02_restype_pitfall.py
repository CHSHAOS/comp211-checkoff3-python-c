"""Step 2: what goes wrong if you skip argtypes/restype.

ctypes cannot read the C header, so it guesses "int" for everything.
"""
import ctypes
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "fastsum.dll" if sys.platform == "win32" else "libfastsum.so"
raw = ctypes.CDLL(os.path.join(os.path.dirname(HERE), NAME))  # no declarations

n = 3_000_000_000
expected = n * (n - 1) // 2
print("expected            :", expected)
try:
    print("without declarations:", raw.sum_range(n))
except Exception as err:  # ctypes may refuse the too-big int argument
    print("without declarations: error ->", type(err).__name__, err)

from load import lib
print("with declarations   :", lib.sum_range(n))
