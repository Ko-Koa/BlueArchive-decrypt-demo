import time
import struct
from typing import Optional


class MersenneTwister:
    # 常量设置
    N = 624
    M = 397
    MATRIX_A = 0x9908B0DF
    UPPER_MASK = 0x80000000
    LOWER_MASK = 0x7FFFFFFF
    AG01 = [0, MATRIX_A]

    def __init__(self, seed: Optional[int] = None) -> None:
        self.mt = [0] * self.N
        self.mti = self.N + 1
        self._init_genrand(seed=seed)

    def NextBytes(self, length: int):
        r = bytearray(length)

        for i in range(0, length, 4):
            b = struct.pack("<I", self._generand_int31())
            for j in range(0, 4):
                k = i + j
                if k >= length:
                    break
                r[k] = b[j]

        return r

    def _init_genrand(self, seed: Optional[int] = None):
        seed = seed or round(time.time() * 1000)
        self.mt[0] = seed & 0xFFFFFFFF

        for mti in range(1, self.N):
            self.mt[mti] = (
                1812433253 * (self.mt[mti - 1] ^ (self.mt[mti - 1] >> 30)) + mti
            )
            self.mt[mti] &= 0xFFFFFFFF

        self.mti = self.N

    def _genrand_int32(self):
        if self.mti >= self.N:
            if self.mti == self.N + 1:
                self._init_genrand(5489)

            for kk in range(self.N - self.M):
                y = (self.mt[kk] & self.UPPER_MASK) | (
                    self.mt[kk + 1] & self.LOWER_MASK
                )
                y &= 0xFFFFFFFF
                self.mt[kk] = self.mt[kk + self.M] ^ (y >> 1) ^ self.AG01[y & 0x1]
                self.mt[kk] &= 0xFFFFFFFF

            for kk in range(self.N - self.M, self.N - 1):
                y = (self.mt[kk] & self.UPPER_MASK) | (
                    self.mt[kk + 1] & self.LOWER_MASK
                )
                self.mt[kk] = (
                    self.mt[kk + (self.M - self.N)] ^ (y >> 1) ^ self.AG01[y & 0x1]
                )
                self.mt[kk] &= 0xFFFFFFFF

            y = (self.mt[self.N - 1] & self.UPPER_MASK) | (self.mt[0] & self.LOWER_MASK)
            self.mt[self.N - 1] = self.mt[self.M - 1] ^ (y >> 1) ^ self.AG01[y & 0x1]
            self.mt[kk] &= 0xFFFFFFFF

            self.mti = 0

        y = self.mt[self.mti]
        self.mti += 1

        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y

    def _generand_int31(self):
        return self._genrand_int32() >> 1 & 0xFFFFFFFF
