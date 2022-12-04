import numpy as np
from geneal.genetic_algorithms import BinaryGenAlgSolver

DAYS_IN_MONTH = 25
EMPLOYEES = 4

UNCOVERED_PENALTY = -10000

MAX_SHIFTS = 8
OVERSHIFT_PENALTY = -5000

def main():
    solver  = BinaryGenAlgSolver(
        n_genes=DAYS_IN_MONTH * EMPLOYEES,
        fitness_function=fitness,
        mutation_rate=0.7,
        selection_rate=0.6,
        pop_size=200,
        max_gen=10000,
    )

    solver.solve()

def fitness(chromosome):
    fitness = 0
    shifts = np.split(chromosome.astype(int), EMPLOYEES)
    
    # check for shift coverage
    coverage = np.zeros(DAYS_IN_MONTH).astype(int)
    for shift in shifts:
        coverage = np.bitwise_or(coverage, shift)
    uncovered_days = DAYS_IN_MONTH - sum(coverage)
    fitness = fitness + uncovered_days * UNCOVERED_PENALTY

    # check for overshift
    for shift in shifts:
        if (sum(shift) > MAX_SHIFTS):
            fitness = fitness + OVERSHIFT_PENALTY
    
    return fitness


if __name__ == '__main__':
    main()
    #print(fitness(np.array([1, 1, 1, 1, 0, 0, 0, 0, 1, 1])))
