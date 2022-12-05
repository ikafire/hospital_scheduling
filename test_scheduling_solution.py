from datetime import date

import numpy as np

from scheduling_solution import SchedulingSolution, Employee

def test_fitness__no_covered_shift__penalty_for_each_uncovered_shift():
    solution = SchedulingSolution(date_start=date(2022, 11, 1), date_end=date(2022, 11, 5))

    fitness = solution.fitness()

    assert fitness == -50000

def test_fitness__partial_coverage__penalty_for_each_uncovered_shift():
    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 5),
        employees=[
            Employee(shift=np.array([0, 1, 0, 0, 0])),
            Employee(shift=np.array([0, 1, 1, 0, 0])),
        ])

    fitness = solution.fitness()

    assert fitness == -30000

def test_fitness__all_covered__no_uncovered_penalty():
    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 5),
        employees=[
            Employee(shift=np.array([1, 1, 1, 0, 0])),
            Employee(shift=np.array([0, 0, 0, 1, 1])),
        ])

    fitness = solution.fitness()

    assert fitness == 0
