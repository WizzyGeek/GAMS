import numpy as np
from .aliases import IntArray

# Only way for this to converge to 0
# is 0 variance
# Not quite First Absolute Central Moment, since it isn't divided by N
# But works for our purposes better (Float approximations and we only use this for ranking)
def first_abs_moment(p: IntArray) -> float:
    mean = np.mean(p)
    return np.sum(np.abs(p - mean))

def predef_moment(p: IntArray, s: int) -> float:
    return sum(abs(s - i) for i in p) # TODO: Numpy

def magic_sums(board: IntArray) -> IntArray:
    return np.concatenate((np.sum(board, axis=0), np.sum(board, axis=1), [np.trace(board), np.sum(board.ravel()[board.shape[0]-1:-1:board.shape[0]-1])]))

# def rank_perm(board: np.ndarray) -> float:
#     sums = magic_sums(board)
#     fam = first_abs_moment(sums)
#     if fam == 0: return 0
#     s = float(np.std(sums))
#     return fam * s

def make_sum(a: int):
    return ((a * a -  1) * a) >> 1

def rank_perm(board: np.ndarray) -> float:
    sums = magic_sums(board)
    fam = predef_moment(sums, make_sum(board.shape[0]))
    if fam == 0: return 0
    s = float(np.std(sums))
    return fam * s

# def perm_stats(board: np.ndarray):
#     sums = magic_sums(board)
#     fam8 = first_abs_moment(sums)
#     stddev = float(np.std(sums))
#     return sums, fam8, stddev

def perm_stats(board: IntArray):
    sums = magic_sums(board)
    pdam = predef_moment(sums, make_sum(board.shape[0]))
    stddev = float(np.std(sums))
    return sums, pdam, stddev