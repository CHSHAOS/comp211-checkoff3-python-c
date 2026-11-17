"""Step 4: time the same work four ways.

  1. pure Python loop
  2. Python built-in sum() (the loop runs in C inside the interpreter)
  3. our C function through ctypes
  4. NumPy (compiled C, with SIMD where the CPU supports it)

Each method runs several times; we report the best (least-disturbed) run.
"""
import ctypes
import statistics
import timeit

import numpy as np
from load import lib

N = 10_000_000
REPEAT = 5

data = np.random.default_rng(0).random(N)
as_list = data.tolist()
ptr = data.ctypes.data_as(ctypes.POINTER(ctypes.c_double))


def python_loop():
    total = 0.0
    for x in as_list:
        total += x
    return total


methods = {
    "pure Python loop": python_loop,
    "built-in sum()": lambda: sum(as_list),
    "C via ctypes": lambda: lib.sum_array(ptr, N),
    "NumPy .sum()": data.sum,
}

# Same answer from every method (floating-point order can differ slightly).
answers = {name: fn() for name, fn in methods.items()}
reference = answers["NumPy .sum()"]
for name, value in answers.items():
    assert abs(value - reference) / reference < 1e-9, (name, value)

print(f"Summing {N:,} doubles, best of {REPEAT} runs\n")
results = {}
for name, fn in methods.items():
    times = timeit.repeat(fn, number=1, repeat=REPEAT)
    results[name] = min(times)
    print(f"{name:18s} best {min(times)*1000:9.2f} ms   median {statistics.median(times)*1000:9.2f} ms")

base = results["pure Python loop"]
print()
for name, t in results.items():
    print(f"{name:18s} {base / t:7.1f}x faster than the Python loop")

# The cost of crossing the Python -> C boundary: call a trivial C function many times.
calls = 1_000_000
t_c = min(timeit.repeat(lambda: lib.add(1, 2), number=calls, repeat=3))
t_py = min(timeit.repeat(lambda: 1 + 2, number=calls, repeat=3))
print(f"\n{calls:,} calls of add(1, 2) through ctypes: {t_c*1000:.0f} ms "
      f"(~{t_c/calls*1e9:.0f} ns per call) vs plain Python 1+2: {t_py*1000:.0f} ms")
