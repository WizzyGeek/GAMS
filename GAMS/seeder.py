import numpy as np
import numpy.typing as npt
from math import log2

from GAMS.aliases import IntArray

dtypes: list[type[np.unsignedinteger]] = [np.uint8, np.uint16, np.uint32, np.uint64]

def select_approprite(n: int):
    bits = int(log2(n)) + 1
    b = 8
    for i in dtypes:
        if bits <= b:
            return i
        b *= 2

    raise Exception("No appropriate type")

def create_population(k: int = 100, l: int = 3, rng: np.random.Generator | None = None, dtype: type[np.unsignedinteger] | None = None) -> list[IntArray]:
    rng = rng or np.random.default_rng()
    dtype = dtype or select_approprite(l * l)
    return [rng.permutation(np.arange(l * l, dtype=dtype)).reshape((l, l)) for _ in range(k)]