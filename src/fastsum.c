/* fastsum.c - small C functions we call from Python with ctypes.
 * Build (Linux/macOS):  gcc -O2 -shared -fPIC -o libfastsum.so src/fastsum.c
 * Build (Windows MinGW): gcc -O2 -shared -o fastsum.dll src/fastsum.c
 */
#include <stddef.h>
#include <stdint.h>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

/* Add two ints: the "hello world" of calling C from Python. */
EXPORT int add(int a, int b) { return a + b; }

/* Sum 0 + 1 + ... + (n-1) with a plain C loop. */
EXPORT int64_t sum_range(int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += i;
    return total;
}

/* Sum an array that Python hands us as a pointer + length.
 * Python owns the memory; C only reads it. */
EXPORT double sum_array(const double *data, size_t len) {
    double total = 0.0;
    for (size_t i = 0; i < len; i++) total += data[i];
    return total;
}

/* Dot product of two arrays of the same length. */
EXPORT double dot(const double *a, const double *b, size_t len) {
    double total = 0.0;
    for (size_t i = 0; i < len; i++) total += a[i] * b[i];
    return total;
}
