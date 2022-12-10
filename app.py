from datetime import date

from scheduling_solution import SchedulingSolution, Employee
from tabu import Tabu

DAYS_IN_MONTH = 31
EMPLOYEES = 7

UNCOVERED_PENALTY = -10000

MAX_SHIFTS = 5
OVERSHIFT_PENALTY = -5000

MAX_ITER = 100


def main():
    tabu = Tabu()
    solution = SchedulingSolution(
        date(2022, 11, 1), date(2022, 11, 30),
        employees=[Employee([0] * 30)])

    result = tabu.solve(solution)

    print(result)


if __name__ == '__main__':
    main()
