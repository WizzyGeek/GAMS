(This is regarding the initial version of this project)

# Genetic Algorithm Magicsquare Search

Using a Genetic Algorithm to find a permutation which is a magic square

## Problems with this experiment

Gamma(10) (aka 9!) is a small number, to remedy we will also run on 4\*4 and 5\*5

## Result

For 3*3 anywhere from epochs worth 1000 to 300 mutations are needed

For 4*4 we were able to find a solution within 63 epochs, it used these mutations
`[wsf(0.8, swap2), wsf(0.9, row_swap), wsf(0.9, col_swap), wsf(0.4, swap3), wsf(0.4, swap_twice), wsf(0.10, no_mut), wsf(0.10, complete_shuffle)]`
and these hyperparameters
```
Mutations per sample: 1
Top k selections: 50
Random selections: 25
Population size: 150
```
and the version this was done on allowed the topk selections to advance without mutations,
The one without allowing, topk to remain took 776 epochs with the same hyperparameters.

another attempt
```
Mutations per sample: 1
Top k selections: 50
Random selections: 20
Population size: 140
```
` [wsf(0.99, swap2), wsf(0.95, swap3), wsf(0.92, swap_twice), wsf(0.10, no_mut), wsf(0.10, complete_shuffle)]`
finished within just 32 epochs

Here is 10 by 10 magic square solution
1000 topk
100 random sampling
2200 population
```
==== Epoch: 682 ====
Top stats:
0 60 38 4 88 55 29 56 73 92
93 87 18 25 61 75 7 84 9 36
35 19 98 45 51 63 82 22 70 10
76 28 89 1 54 34 90 72 20 31
81 64 62 85 46 2 6 42 16 91
71 14 26 17 48 66 69 57 41 86
21 50 67 97 3 79 24 12 43 99
15 53 11 96 39 65 58 74 52 32
59 80 8 30 68 33 83 27 94 13
44 40 78 95 37 23 47 49 77 5
sums: [495 495 495 495 495 495 495 495 495 495 495 495 495 495 495 495 495 495
 495 495 495 495]
fam: 0.0
stddev: 0.0
Found 0 more best samples.
```

Here is a better 4 by 4 solution
```
==== Epoch: 22 ====
Top stats:
11 6 5 8
2 12 15 1
13 3 0 14
4 9 10 7
sums: [30 30 30 30 30 30 30 30 30 30]
fam: 0.0
stddev: 0.0
Found 1 more best samples.
```
`[wsf(2, swap2), wsf(1.7, swap3), wsf(1.5, swap_twice), wsf(0.1, complete_shuffle), wsf(0.3, no_mut), wsf(0.6, row_swap), wsf(0.6, col_swap)]`
```
Mutations per sample: 3
Top k selections: 50
Random selections: 200
Population size: 1000
```
This run explored 22 * 750 mutations at max which is `16500`

And here is the last run

```
==== Epoch: 8 ====
Top stats:
6 12 9 3
1 11 14 4
10 0 5 15
13 7 2 8
sums: [30 30 30 30 30 30 30 30 30 30]
fam: 0.0
stddev: 0.0
Found 0 more best samples.
```
```
Mutations per sample: 19
Top k selections: 10
Random selections: 40
Population size: 1000
```
This run only explored 8 * 900 mutations `7200` mutations

From this limited data I conclude that this simplistic single parent genetic algorithm converges faster for higher mutation per sample
and higher random sampling.

## Conclusion

Even Simple Genetic Algos can speed up a search, albeit possibly not comprably to the sophisticated ones, but more sped up than simply naive pruning.

2nd, You have to be careful in you score the samples  
3rd, You have to combat falling into a local minima  
4th, find balance between population size and speed.  
It's more headache than it's worth
