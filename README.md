<h1 align="center">
    GAMS
</h1>

<div align="center">
    Genetic Algorithm Magicsquare Search
</div>

## About
This is my experiment to test how Genetic Algorithms can be used
to speed up search. This repo uses a very simplistic approach to solve
a simple problem, to search for magic squares.

### Why Magic Squares?

Magic squares make the perfect candidate for testing the efficacy of
genetic algorithms. The state space grows very huge by the relation
`(s * s)!`, where s is side of the square, and the number of solutions
gets more and more sparse

## Results

The search was relatively fast for small boards, but on larger boards
the chance of getting stuck on a local minima was greater, upon hitting
a minima for the larger boards you would have to increase the mutation
rate to essentially start again.

The crossover function, even though it is not very domain specific,
helped a lot is speeding up search, its addition was very noticable as
it quickly converged to any minimas.

I usually like to crossover about 70% to 80% of the population,
and the rest generated by mutation, this is because sometimes we are
extremely close to solving the problem and crossover may yield
 outlandish answers. Further lengthening the search

I am not sure if k way selection actually has any significant benefits,
a more detailed statistical study will be needed to conclude anything
regarding k-way selection.