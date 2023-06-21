from typing import IO
from .aliases import IntArray
from .ranker import perm_stats

def epoch_start(epoch: int):
    print("="*4, "Epoch:", epoch, "="*4)

def best_found(p: IntArray):
    print("Best Found in epoch")
    print("\n".join(" ".join(str(c) for c in d) for d in p))

def stats(p: IntArray, fp: IO[str] | None = None):
    st = perm_stats(p)
    print("\n".join(" ".join(str(c) for c in d) for d in p), file=fp)
    print("sums:", st[0], file=fp)
    print("fam:", st[1], file=fp)
    print("stddev:", st[2], file=fp)
    return st[1]