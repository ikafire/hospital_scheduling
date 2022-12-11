from datetime import date
from collections import Counter
import itertools

from scheduling_solution import SchedulingSolution, Employee
from tabu import Tabu

DAYS_IN_MONTH = 31
EMPLOYEES = 7

UNCOVERED_PENALTY = -10000

MAX_SHIFTS = 5
OVERSHIFT_PENALTY = -5000

MAX_ITER = 100


def main():
    tabu = Tabu(max_iter=50)
    solution = SchedulingSolution(
        date(2022, 12, 1), date(2022, 12, 30),
        employees=[
            Employee('✚', days_off=[date(2022, 12, 2), date(2022, 12, 3), date(2022, 12, 4), date(2022, 12, 5), date(2022, 12, 6), date(2022, 12, 7), date(2022, 12, 8), date(2022, 12, 9), date(2022, 12, 10), date(2022, 12, 11), date(2022, 12, 12), date(2022, 12, 13), date(2022, 12, 14), date(2022, 12, 15), date(2022, 12, 16), date(2022, 12, 17), date(2022, 12, 18), date(2022, 12, 22), date(2022, 12, 24)]),
            Employee('❖', days_off=[date(2022, 12, 2), date(2022, 12, 3), date(2022, 12, 6), date(2022, 12, 15), ]),
            Employee('§', days_off=[date(2022, 12, 4), date(2022, 12, 10), date(2022, 12, 24), date(2022, 12, 25), ]),
            Employee('⌘', days_off=[date(2022, 12, 9), date(2022, 12, 10), date(2022, 12, 21), date(2022, 12, 23), date(2022, 12, 28)]),
            Employee('✿', days_off=[date(2022, 12, 8), date(2022, 12, 9), date(2022, 12, 10), date(2022, 12, 25), ]),
            Employee('❆', days_off=[date(2022, 12, 10), date(2022, 12, 16), date(2022, 12, 17), date(2022, 12, 18), ]),
            Employee('◒', days_off=[date(2022, 12, 4), date(2022, 12, 10)]),
            Employee('⍟', days_off=[date(2022, 12, 2), date(2022, 12, 3), date(2022, 12, 4), date(2022, 12, 12), date(2022, 12, 21)]),
            Employee('λ', capacities=['病房'], days_off=[date(2022, 12, 2), date(2022, 12, 3), date(2022, 12, 4), date(2022, 12, 16), date(2022, 12, 30)]),
            Employee('急', capacities=['病房'], days_off=[date(2022, 12, 9), date(2022, 12, 16), date(2022, 12, 30), date(2022, 12, 31)]),
            Employee('Y1', capacities=['病房'], days_off=[date(2022, 12, 21), date(2022, 12, 27), date(2022, 12, 28), date(2022, 12, 31)]),
            ],
        shift_types=['病房', 'ICU', '急診'])

    result = tabu.solve(solution)

    print(f'final fitness: {result.fitness()}')
    print(f'病房: {result.shifts["病房"]}')
    print(f'ICU: {result.shifts["ICU"]}')
    print(f'急診: {result.shifts["急診"]}')
    print(Counter(itertools.chain(*result.shifts.values())))


if __name__ == '__main__':
    main()
