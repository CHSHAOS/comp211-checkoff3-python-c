"""Step 1: call a C function from Python."""
from load import lib

print("add(2, 3) =", lib.add(2, 3))
print("sum_range(10) =", lib.sum_range(10))  # 0+1+...+9 = 45
