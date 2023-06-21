import random
from types import FunctionType
import numpy as np
import typing as t

from .aliases import IntArray

def idx(a: int, col: int) -> tuple[int, int]: return (a // col, a % col)

def no_mut(p: IntArray) -> IntArray:
    return p

def col_swap(p: IntArray) -> IntArray:
    a = random.randint(0, p.shape[1] - 1)
    b = random.randint(0, p.shape[1] - 2)
    if b >= a: b += 1
    ret = p.copy()
    ret[:, a] = p[:, b]
    ret[:, b] = p[:, a]
    return ret

def row_swap(p: IntArray) -> IntArray:
    a = random.randint(0, p.shape[0] - 1)
    b = random.randint(0, p.shape[0] - 2)
    if b >= a: b += 1
    ret = p.copy()
    ret[a] = p[b]
    ret[b] = p[a]
    return ret

def swap2(p: IntArray) -> IntArray:
    a = random.randint(0, p.size - 1)
    b = random.randint(0, p.size - 2)
    if b >= a: b += 1
    ret = p.copy()
    col = p.shape[1]
    ret[idx(a, col)] = p[idx(b, col)]
    ret[idx(b, col)] = p[idx(a, col)]
    return ret

def swap3(p: IntArray) -> IntArray:
    # distinct and random
    a = random.randint(0, len(p) - 1)
    b = random.randint(0, len(p) - 2)
    if b >= a: b += 1
    c = random.randint(0, len(p) - 3)
    if c >= a:
        c += 1
    if c >= b:
        c += 1

    ret = p.copy()
    col = p.shape[1]
    ret[idx(a, col)] = p[idx(c, col)]
    ret[idx(b, col)] = p[idx(a, col)]
    ret[idx(c, col)] = p[idx(b, col)]
    return ret

def swap_twice(p: IntArray) -> IntArray:
    a = random.randint(0, len(p) - 1)
    b = random.randint(0, len(p) - 2)
    if b >= a: b += 1
    c = random.randint(0, len(p) - 1)
    d = random.randint(0, len(p) - 2)
    if d >= c: d += 1

    ret = p.copy()
    col = p.shape[1]
    ret[idx(a, col)] = p[idx(b, col)]
    ret[idx(b, col)] = p[idx(a, col)]
    e = ret[idx(c, col)]
    ret[idx(c, col)] = ret[idx(d, col)]
    ret[idx(d, col)] = e
    return ret

def complete_shuffle(p: IntArray) -> IntArray:
    return np.random.permutation(p)

def weighted_swap_factory(relative_wt: float, swapper: t.Callable[[IntArray], IntArray]) -> t.Callable[[IntArray], IntArray]:
    swap = FunctionType(swapper.__code__, globals())
    swap.wt = relative_wt # type: ignore
    return swap