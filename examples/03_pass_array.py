"""Step 3: hand a whole array to C as a pointer, like passing int *arr in COMP 211."""
import ctypes
import numpy as np
from load import lib

values = [1.5, 2.5, 3.0, 4.0]

# Option A: build a C array by hand.
c_array = (ctypes.c_double * len(values))(*values)
print("C array          :", lib.sum_array(c_array, len(values)))

# Option B: a NumPy array already stores its numbers as one contiguous C buffer,
# so we can just pass a pointer to that buffer. No copy is made.
arr = np.array(values, dtype=np.float64)
ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
print("NumPy buffer     :", lib.sum_array(ptr, arr.size))
print("NumPy's own sum  :", arr.sum())
