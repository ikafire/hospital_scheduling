from datetime import date

from asq import query
from pytest_unordered import unordered
import pytest

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
            Employee(shift=[0, 1, 0, 0, 0]),
            Employee(shift=[0, 1, 1, 0, 0]),
        ])

    fitness = solution.fitness()

    assert fitness == -30000

def test_fitness__all_covered__no_uncovered_penalty():
    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 5),
        employees=[
            Employee(shift=[1, 1, 1, 0, 0]),
            Employee(shift=[0, 0, 0, 1, 1]),
        ])

    fitness = solution.fitness()

    assert fitness == 0

def test_get_neighbors__one_employee__modify_one_shift_at_a_time():
    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 3),
        employees=[
            Employee(shift=[0, 0, 0]),
        ])

    neighbors = solution.get_neighbors()
    neighbor_shifts = query(neighbors).select(lambda n: ''.join(map(str, n.employees[0].shift))).to_list()

    assert len(neighbors) == 3
    assert neighbor_shifts == unordered(['100', '010', '001'])


@pytest.mark.parametrize("left,right,expected", [
    (SchedulingSolution(date(2022, 11, 1), date(2022, 11, 3)), SchedulingSolution(date(2022, 11, 1), date(2022, 11, 4)), False),
    (SchedulingSolution(date(2022, 11, 1), date(2022, 11, 3)), SchedulingSolution(date(2022, 11, 1), date(2022, 11, 3)), True),
    (SchedulingSolution(date(2022, 11, 1), date(2022, 11, 3), employees=[Employee(id='a', shift=[1, 1, 0])]), SchedulingSolution(date(2022, 11, 1), date(2022, 11, 3), employees=[Employee(id='a', shift=[1, 0, 0])]), False),
    (SchedulingSolution(date(2022, 11, 1), date(2022, 11, 3), employees=[Employee(id='a', shift=[1, 1, 0])]), SchedulingSolution(date(2022, 11, 1), date(2022, 11, 3), employees=[Employee(id='a', shift=[1, 1, 0])]), True),
    (SchedulingSolution(date(2022, 11, 1), date(2022, 11, 3), employees=[Employee(id='a', shift=[1, 1, 0])]), SchedulingSolution(date(2022, 11, 1), date(2022, 11, 3), employees=[Employee(id='b', shift=[1, 1, 0])]), False),
])
def test_solution_equal(left, right, expected):
    assert left.__eq__(right) == expected
