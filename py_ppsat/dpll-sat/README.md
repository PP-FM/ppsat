# Complete SAT Solver Practice
Simple COMPLETE SAT Solver. \
You can find a copy of this repository at https://github.com/markankaro/dpll-sat/. 

## Solvers

```
$ python solvers/<solver_name> <formula_to_solve> *[<branching_heuristic>]
```
\**only for base_sat.py*


Solvers list:
* solver_exp.py : experimental solver (too slow and not working)
* original_dpll.py : base solver, random selection
* base_sat.py : solver with more branching heuristics
* linked_sat.py : solver with linked list structure (only with JW branching heuristic)
* race_sat.py : base_solver with 2 sided jeroslow wang branching heuristic
* noflags_linked_sat.py : faster version of linked_sat.py without flags

### base_sat branching heuristics
* **FRE** (Freeman) : counts both the number of positive l and negative -l occurrences of a given variable l.
* **RAN** (Random) : random selectionrm
* **MO** (Most often) : counts the occurrences of each l literal
* **JW** (Jeroslow Wang) : let C be the set of open clauses containing a single polarity of a given variable l. Then to the given variable l a weight of the summation of 2^(length of c) for each c ∈ C.
* **JW2S** (2 sided Jeroslow Wang) : Jeroslow Wang but C contains either polarity of a given variable.
* **SPC** (Shortest Positive Clause) : searches for the shortest clause with all literals positive.


## Utils
### Formula generator


CNF formula generator, [DIMACS format].

```
$ python utils/rnd_cnf_gen.py <num_vars> <num_clauses> <clauses_length> [<seed>] [ > file ]
```

### Benchmarks tester

Test a folder of CNF formulas and get the average time with a solver and heuristic.

```
$ ./utils/test_benchmarks.sh <benchmark_folder> <solver_name> *[<heurisitc>]
```
\**only for base_sat.py*

Example:
```
$ chmod +x utils/test_benchmarks.sh
$ ./utils/test_benchmarks.sh benchmark/dubois solvers/base_sat.py JW2S
```

### Solution validator

Validator for SATISFIABLE formulas, [DIMACS format]. 

```
$ python utils/sat_val.py <formula> <solution>
```

[DIMACS format]: http://www.satcompetition.org/2004/format-solvers2004.html
