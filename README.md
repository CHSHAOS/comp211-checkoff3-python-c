# Python Libraries Implemented in C

COMP 211 Checkoff 3 — Qiang Shao

Python is easy to write but slow at tight number-crunching loops. Libraries like
NumPy get around this by doing the heavy work in compiled C. This repo explores
how that works: writing a C function, compiling it into a shared library,
calling it from Python with `ctypes`, and measuring how much faster it is.

> **Why I picked this topic:** _TODO (in your own words, e.g. your Slay the Spire
> AI project calls a compiled simulator from Python)._

## What's in here

| File | What it shows |
|---|---|
| `src/fastsum.c` | Four small C functions: `add`, `sum_range`, `sum_array`, `dot` |
| `examples/load.py` | Loads the compiled library and declares each function's argument/return types |
| `examples/01_hello_ctypes.py` | Calling C from Python for the first time |
| `examples/02_restype_pitfall.py` | What breaks if you don't tell `ctypes` the types |
| `examples/03_pass_array.py` | Passing a whole array to C as a pointer, including NumPy's own buffer |
| `examples/04_benchmark.py` | Timing a Python loop vs `sum()` vs our C code vs NumPy |
| `slides/` | Presentation slides |

## How to run

You need `gcc`, Python 3, and NumPy (`pip install numpy`).

```bash
# Linux / macOS / the COMP 211 container
gcc -O2 -Wall -Wextra -shared -fPIC -o libfastsum.so src/fastsum.c

# Windows (MinGW)
gcc -O2 -Wall -Wextra -shared -o fastsum.dll src/fastsum.c

cd examples
python 01_hello_ctypes.py
python 02_restype_pitfall.py
python 03_pass_array.py
python 04_benchmark.py
```

## Results

Summing 10,000,000 doubles, best of 5 runs (Windows 11, Python 3.12.10, gcc 16.1 `-O2`, NumPy 2.5.1):

| Method | Time | Speedup vs Python loop |
|---|---:|---:|
| Pure Python `for` loop | 107.0 ms | 1.0x |
| Built-in `sum()` | 37.3 ms | 2.9x |
| Our C function via `ctypes` | 3.9 ms | 27.6x |
| NumPy `.sum()` | 4.3 ms | 24.9x |

Calling a trivial C function (`add(1, 2)`) one million times through `ctypes`
took 234 ms, about **234 ns per call**, compared with 13 ms for doing `1 + 2` in Python.

## Things I found interesting

1. **The speedup comes from where the loop runs.** In the Python loop, every `+=`
   is an interpreter step on a boxed Python object. In C, the same loop is a few
   machine instructions on raw `double`s in one contiguous block of memory.
2. **Crossing into C has a fixed cost.** Each `ctypes` call converts Python objects
   to C values and back. That's why you pass a whole array to C once, instead of
   calling C once per element. NumPy follows the same rule: one call, one big loop in C.
3. **`ctypes` trusts you about types.** It can't read the C header, so it assumes
   every argument and return value is an `int`. Without `restype = c_int64`,
   `sum_range(3_000_000_000)` returned `400150784` instead of
   `4499999998500000000`, with no error at all.
4. **A NumPy array is already a C array.** `arr.ctypes.data_as(...)` gives C a pointer
   to NumPy's buffer with no copying. This is the same `double *` + length pattern
   from COMP 211.

## Resources

- Python docs, `ctypes` — https://docs.python.org/3/library/ctypes.html
- NumPy docs, "NumPy: the absolute basics" and "Interfacing with C" — https://numpy.org/doc/stable/
- Dive into Systems (COMP 211 textbook), chapters on C arrays and pointers — https://diveintosystems.org/
- Python docs, `timeit` — https://docs.python.org/3/library/timeit.html
