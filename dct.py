import numpy as np
from scipy.fft import dct, idct

def GetH():
    n = 8
    a = np.random.randint(0, 100, (n, n))

    h = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == 0:
                h[i][j] = np.sqrt(1 / n)
            else:
                h[i][j] = np.sqrt(2 / n)*np.cos(np.pi * (2 * j + 1) * i / (2 * n))

    return h

H = GetH()

def DCT(a):
    global H
    h = H
    c = np.matmul(np.matmul(h, a), np.transpose(h))

    return c

def IDCT(c):
    global H
    h = H
    a = np.matmul(np.matmul(np.transpose(h), c), h)

    return np.int32(a)

'''
a = np.array([
    [-5, -7, -6, -3, 6, 12, 16, 17],
    [-3, -6, -6, -3, 6, 12, 15, 15],
    [1, -3, -5, -1, 5, 13, 14, 13],
    [3, -1, -4, 0, 6, 12, 15, 14],
    [4, 1, 0, 2, 7, 12, 15, 15],
    [4, 3, 3, 5, 8, 12, 16, 18],
    [4, 5, 7, 8, 9, 12, 17, 20],
    [5, 7, 9, 9, 9, 11, 16, 22]
])
print(a)
c = DCT(a)
import quantization as q

c = q.Quantize(c)
print(c)
c = q.Dequantize(c)

#print(c)
s = IDCT(c)

print(s)
'''