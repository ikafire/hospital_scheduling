import numpy as np
from geneal.genetic_algorithms import BinaryGenAlgSolver

DAYS_IN_MONTH = 31
EMPLOYEES = 7

UNCOVERED_PENALTY = -10000

MAX_SHIFTS = 5
OVERSHIFT_PENALTY = -5000

MAX_ITER = 100

def get_zeroes():
    return np.zeros(DAYS_IN_MONTH * EMPLOYEES).astype(int)

def get_string_notation(solution):
    return ''.join(solution.astype(str))

def print_readable_notation(solution):
    shifts = split_solution_to_shifts(solution)
    for i, shift in enumerate(shifts):
        print(f'doc {i}: {get_string_notation(shift)}, shift count: {sum(shift)}')

def main():
    best_solution = get_zeroes()
    best_fitness = fitness(best_solution)
    current_solution = best_solution
    current_fitness = fitness(current_solution)
    tabu_list = set()
    tabu_list.add(get_string_notation(best_solution))

    i = 0
    while i < MAX_ITER and best_fitness < 0:
        neighbors = get_neighbors(current_solution)
        current_solution = neighbors[0]
        current_fitness = fitness(current_solution)
        for neighbor in neighbors:
            str_form = get_string_notation(neighbor)
            neighbor_fitness = fitness(neighbor)
            if (not str_form in tabu_list) and neighbor_fitness > current_fitness:
                current_solution = neighbor
                current_fitness = neighbor_fitness
    
        if current_fitness > best_fitness:
            best_solution = current_solution
            best_fitness = current_fitness
        
        tabu_list.add(get_string_notation(current_solution))

        i = i + 1
        print(f'iter {i}')
        print(f'best solution: {best_solution}, fitness {best_fitness}')
        print(f'current solution: {current_solution}, fitness {current_fitness}')

    return best_solution

def get_neighbors(solution):
    import random

    neighbors = []
    for i in range(solution.size):
        x = solution.copy()
        if x[i] == 0:
            x[i] = 1
        else:
            x[i] = 0
        neighbors.append(x)

    random.shuffle(neighbors)
    return neighbors

def fitness(solution):
    fitness = 0
    shifts = split_solution_to_shifts(solution)
    
    # shift coverage penalty
    coverage = np.zeros(DAYS_IN_MONTH).astype(int)
    for shift in shifts:
        coverage = np.bitwise_or(coverage, shift)
    uncovered_days = DAYS_IN_MONTH - sum(coverage)
    fitness = fitness + uncovered_days * UNCOVERED_PENALTY

    # overshift penalty
    for shift in shifts:
        if (sum(shift) > MAX_SHIFTS):
            fitness = fitness + OVERSHIFT_PENALTY
    
    shift_days = [sum(shift) for shift in shifts]
    # total shift count penalty
    fitness = fitness - np.sum(shift_days)
    # fairness penalty
    fitness = fitness - np.var(shift_days)

    return fitness

def split_solution_to_shifts(solution):
    return np.split(solution.astype(int), EMPLOYEES)


if __name__ == '__main__':
    print_readable_notation(main())
