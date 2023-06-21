import random

import GAMS.seeder
import GAMS.generation
from GAMS.mutations import weighted_swap_factory as wsf, swap2, swap3, swap_twice
from GAMS.ranker import rank_perm
from GAMS.interface import stats, epoch_start
from GAMS.crossover import oxc


def print_individual(ind: GAMS.generation.Individual, fp=None):
    stats(ind.data, fp)
    print("Ranking: ", ind.ranking, file=fp)
    print("Age: ", ind.age, file=fp)

def main():
    l = int(input("Board Size: "))
    topk = int(input("Top k: "))
    k = int(input("Population size: "))
    kway_k = int(input("K way selection k (selection pressure, 3 is good): "))
    pop = GAMS.seeder.create_population(k=k, l=l)
    muts = [wsf(2, swap2), wsf(1.7, swap3), wsf(1.5, swap_twice)]
    # muts = [swap2, swap3, swap_twice, complete_shuffle, no_mut]

    pop = GAMS.generation.Population(rank_perm, pop, topk, k, muts, oxc, kway_k=kway_k)

    print("Epoch 0")
    print("Population size:", pop.size)
    print("Best Sample:")
    pop.population.sort()
    stats(pop.population[0].data)

    loops = 0
    epoch = 1
    while 1:
        try:
            if loops <= 0:
                try:
                    r = input("Enter a number or command | ")
                    if r.lower() in {"q", "quit", "exit", "e"}:
                        return
                    elif r.lower()[:4] == "topk":
                        a = int(r[5:])
                        if a < k:
                            pop.topk = a
                            print("Updated topk")
                        else: print("Invalid topk value, size is ", k)
                    elif r.lower()[:5] == "cross":
                        a = float(r[6:])
                        if 0 <= a <= 1:
                            pop.cross_percent = a
                            print("Updated 'crossiness'")
                        else: print("Invalid value", a, "Expected between 0 to 1")
                    elif r.lower()[:3] == "mut":
                        a = float(r[4:])
                        if 0 <= a <= 1:
                            pop.mutation_prob = a
                            print("Updated mutation probability")
                        else: print("Invalid value", a, "Expected between 0 to 1")
                    elif r.lower()[:3] == "age":
                        a = int(r[4:])
                        if a > 0:
                            pop.max_top_age = a
                            print("Updated max top age")
                        else:
                            print("Invalid age", a, "Expected positive integer")
                    elif r.lower() == "config":
                        print("Population: ", pop.size)
                        print("Topk: ", pop.topk, f"{(pop.topk/pop.size):2.2%}")
                        print("Max Top age: ", pop.max_top_age)
                        print(f"Mutation Chance: {pop.mutation_prob:2.2%}")
                        print(f"Cross percentage: {pop.cross_percent:2.2%}")
                    elif r.lower() == "explore":
                        print("1. Random Sampling\n2. K way tournament\n3. topk\n4. All")
                        r = int(input("Mode: "))
                        fname = input("File name: ")
                        fp = open(fname, "w")
                        n = 0
                        if r != 4:
                            n = int(input("Number of samples: "))
                        else:
                            n = len(pop.population)

                        if r == 1:
                            for i in random.sample(pop.population, k=n):
                                print("====", file=fp)
                                print_individual(i, fp)
                        elif r == 2:
                            k = int(input("K way k: "))
                            if k <= 0:
                                print("Invalid k value")
                                fp.close()
                                continue

                            if k > 1:
                                for _ in range(n):
                                    i = pop.population[pop.kway_select(k)]
                                    print("====", file=fp)
                                    print_individual(i, fp)
                            else:
                                l = len(pop.population) - 1
                                for _ in range(n):
                                    i = pop.population[random.randint(0, l)]
                                    print("====", file=fp)
                                    print_individual(i, fp)
                        elif r == 3 or r == 4:
                            for i in pop.population[:min(n, len(pop.population))]:
                                print("====", file=fp)
                                print_individual(i, fp)
                        fp.close()
                    else:
                        loops = int(r)
                except Exception:
                    continue
            else:
                epoch_start(epoch)
                pop.next_gen()
                print("Top stats:")
                fam = stats(pop.population[0].data)
                print("Ranking: ", pop.population[0].ranking)
                print("Age: ", pop.population[0].age)
                if fam == 0:
                    loops = 0
                    found = 0
                    for i in pop.population[1:]:
                        if i.ranking == 0: found += 1
                        else: break
                    print("Found", found, "more best samples.")
                epoch += 1
                loops -= 1
        except KeyboardInterrupt:
            loops = 0

main()