# SAT-SOLVE Program
## About
This program is part of my Logic Coursework which I needed to implement SAT-SOLVE program in Python under given conditions. The program passed all the unit tests, the `dpll_sat_solve(()` function run faster than the benchmark code, giving me perfect score for this part.

## Introduction
The file `engine.py` contains the core components of the program.
- `load_dimac()` function allows to convert files in dimac form to a list of clauses
- `simple_sat_solve()` function to solve the instance naively
- `branching_sat_solve()` function to solve the instance by branching
- `unit_propagate()`: reduce the redudant clauses by unit propagation
- `dpll_sat_solve()`: branching Sat-Solve with Unit Propataion for optimisation

