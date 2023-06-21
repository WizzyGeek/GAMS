# Deduplication Benchmark

# If you have a fast, strong hash function for permutations
# Dont hesitate to open a PR

from functools import reduce
from time import process_time

from GAMS.generation import Individual
from GAMS.seeder import create_population
from GAMS.ranker import rank_perm

import numpy as np
import random

n = 100
dup = 9
a = create_population(n)
a = np.concatenate((a, random.choices(a, k=int(n * dup))))

b = [Individual(i, rank_perm(i)) for i in a]

# Test with default Hash function

def dedup(b): # Emulate our workload
    ps = set()
    for i in b:
        if i not in ps:
            ps.add(i)
    return ps

def bench(b):
    k = 100
    t = 0
    for i in range(k):
        now = process_time()
        dedup(b)
        t += process_time() - now
    return t / k

hl = list(bench(b) for _ in range(10))
hh = sum(hl) / 10
print(hh, max(hl) / min(hl), min(hl), max(hl))

def cantor_hash0(self: Individual):
    return reduce(lambda a, b: (((a + b) * (a + b + 1)) >> 1) + b , map(int, self.data.flat))

def cantor_hash(self: Individual):
    it = iter(map(int, self.data.flat))
    a = next(it)
    for i in it:
        a = (((a + i) * (a + i + 1)) << 1) + i
    return a

Individual.__hash__ = cantor_hash0

hl = list(bench(b) for _ in range(10))
hh = sum(hl) / 10
print(hh, max(hl) / min(hl), min(hl), max(hl))