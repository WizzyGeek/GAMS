
import numpy as np
from .aliases import IntArray
import random

# Wanted to make OX1 but this was just easier to make,
# and I dont mind
def oxc_idx_mask(n: int) -> list[int]:
    r = random.getrandbits(n)
    idx = 0
    m = []
    while r > 0:
        if r & 1:
            m.append(idx)
        r >>= 1
        idx += 1
    return m


def oxc(p1: IntArray, p2: IntArray) -> IntArray:
    ret = p1.copy()
    m = oxc_idx_mask(p1.size) # Controls The type of Cross Over
    t = p1.ravel()[m]
    ret.ravel()[m] = [i for i in p2.ravel() if i in t] # Maybe Speed up
    return ret
