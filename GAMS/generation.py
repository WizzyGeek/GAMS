from __future__ import annotations

import typing as t
from itertools import accumulate
from functools import reduce
import random

import numpy as np

from .aliases import IntArray

# Leader Board System
# Top k Performers Remain on leaderboard
# Top_K + Population next_gen Created
# (How?)
#  top_k will be allowed to go to next gen as is. (population left now)
#  Replace entire Population
#  2 Modes
#  - Single Parent, Dual Parent
#    Single Parent Mutation Only
#    Dual Parent Crossover + mutation
#    How to Dual Parent?
#     Make Selection Pool (all added)
#       k way selection
#     Select 2 Parents
#     Crossover
#     Introduce Mutation
#     Add to New Population
#   How to single Parent
#    Optional Make Selection **slighly** biased towards topk (Challenge the topk rankings before individual dies of age)
#    Introduce Mutation
#    Add to new population
#  Do k way selection and attempt crossing
#  Failure Condition: Too similar
#  On failure move on
#  for n failures
#  Do single parent, biased toward topk maybe
# Age Update
# Prune Old, Generate Children
# Rerank
# Leaderboard Update
# Repeat

# Let there be crossovers/mutation which completely randomize
# And crossovers/mutations which return copies (hope more converengence next epoch, keep chances low)

class Individual:
    __slots__ = ("data", "ranking", "age")

    data: IntArray
    ranking: float
    age: int

    def __init__(self, data: IntArray, ranking: float) -> None:
        self.data = data
        self.ranking = ranking
        self.age = 0

    def __lt__(self, o: Individual): # end up first on sorting
        return self.ranking < o.ranking

    def __eq__(self, o: Individual):
        if self.ranking == o.ranking:
            return np.array_equal(self.data, o.data)
        return False

    def __gt__(self, o: Individual):
        return self.ranking > o.ranking

    def __hash__(self) -> int:
        return reduce(lambda a, b: (a << 1) ^ b, map(int, self.data.flat))

class Population:
    def __init__(self, ranker: t.Callable[[IntArray], float],
                 population: list[IntArray],
                 topk: int,
                 target_size: int,
                 mutation_funcs: list[t.Callable[[IntArray], IntArray]],
                 crossover_func: t.Callable[[IntArray, IntArray], IntArray],
                 max_top_age: int = 100,
                 mutation_prob: float = 0.9,
                 cross_percent: float = 0.25,
                 kway_k: int = 3):
        self.ranker = ranker
        self.population = list(map(lambda p: Individual(p, ranker(p)), population))
        self.size = target_size
        self.mutations = mutation_funcs
        self.mut_wts = list(accumulate([getattr(i, "wt", 1) for i in mutation_funcs]))
        self.crossover = crossover_func
        self.max_top_age = max_top_age
        self.mutation_prob = mutation_prob
        self.cross_percent = cross_percent
        self.topk = topk
        self.kway_k = kway_k

    def kway_select(self, k: int) -> int:
        # The PDF looks like x^(k-1)
        # TODO: Can consume less random?
        # https://stackoverflow.com/questions/72693182/how-to-generate-a-single-random-number-given-a-continuous-pdf-in-python

        return min(*(random.randint(0,len(self.population) - 1) for _ in range(k)))

    def next_gen(self) -> None:
        topk = self.topk
        population = self.population
        if topk > self.size:
            raise ValueError("Topk greater than size of population")

        # population.sort()

        pop = population[:topk] # Leaderboard
        extra = 0
        i = 0
        while i < len(pop):
            a = pop[i]
            if a.age >= self.max_top_age:
                pop.pop(i)
                extra += 1
                continue
            a.age += 1
            i += 1

        ps = set(pop)

        i = extra
        l = len(population)
        while i > 0:
            mut = random.choices(self.mutations, cum_weights=self.mut_wts, k=1)[0](population[random.randint(0, l - 1)].data)
            ind = Individual(mut, self.ranker(mut))
            if ind not in ps:
                ps.add(ind)
                i -= 1

        i = cross_num = max(int((self.size - topk) * self.cross_percent), 0)

        while i > 0:
            crossed = self.crossover(population[self.kway_select(self.kway_k)].data, population[self.kway_select(3)].data)
            if random.random() <= self.mutation_prob:
                crossed = random.choices(self.mutations, cum_weights=self.mut_wts, k=1)[0](crossed)

            ind = Individual(crossed, self.ranker(crossed))
            if not (ind in ps):
                ps.add(ind)
                i -= 1

        for idx, mutation in enumerate(random.choices(self.mutations, cum_weights=self.mut_wts, k=(self.size - topk - cross_num)), topk):
            if random.random() <= self.mutation_prob:
                mut = mutation(population[idx % l].data)
                ind = Individual(mut, self.ranker(mut))
                i = 0
                while (ind in ps) and i < 5:
                    mut = mutation(population[idx % l].data)
                    ind = Individual(mut, self.ranker(mut))
                    i += 1
                if i >= 5:
                    continue # drop this iteration
                if ind not in ps:
                    ps.add(ind)
            else:
                t = population[idx % l]
                t.age += 1
                if t in ps:
                    k = list(ps.intersection((t,)))
                    assert len(k) == 1
                    k[0].age = t.age
                else:
                    ps.add(t)

        self.population = list(ps)
        self.population.sort()
