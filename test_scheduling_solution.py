from datetime import date

from pytest_unordered import unordered
import pytest

from scheduling_solution import SchedulingSolution, Employee


def test_shifts__no_initial_shifts__initialize_shift_with_arbitrary_assignment():
    def assert_shift(shift):
        assert len(shift) == 3  # day count
        assert all(element in ('A', 'B') for element in shift)

    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 3),
        shift_types=['type1', 'type2'],
        employees=[
            Employee(name='A'),
            Employee(name='B'),
        ])

    assert_shift(solution.shifts['type1'])
    assert_shift(solution.shifts['type2'])


def test_shifts__no_initial_shifts_and_limitations__initialize_shift_not_violating_limitations():
    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 2),
        shift_types=['type1', 'type2'],
        employees=[
            Employee(name='A', capacities=['type1']),
            Employee(name='B', capacities=['type2'], days_off=[date(2022, 11, 2)]),
            Employee(name='C', capacities=['type2'], days_off=[date(2022, 11, 1)]),
        ])

    assert solution.shifts == {'type1': ['A', 'A'], 'type2': ['B', 'C']}


def test_shifts__given_initial_shifts__return_initial_shifts():
    initial_shifts = {'type1': ['A', 'B', 'A'], 'type2': ['B', 'A', 'B']}
    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 3),
        shift_types=['type1', 'type2'],
        employees=[
            Employee(name='A'),
            Employee(name='B'),
        ],
        initial_shifts=initial_shifts)

    assert solution.shifts == initial_shifts


def test_get_neighbors__always__change_one_slot_at_a_time():
    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 3),
        shift_types=['type1', 'type2'],
        initial_shifts={'type1': ['A', 'A', 'A'], 'type2': ['A', 'A', 'A']},
        employees=[
            Employee(name='A'),
            Employee(name='B'),
            Employee(name='C'),
        ])

    neighbors = solution.get_neighbors()
    neighbor_shifts = [n.shifts for n in neighbors]

    assert neighbor_shifts == unordered([
        {'type1': ['B', 'A', 'A'], 'type2': ['A', 'A', 'A']},
        {'type1': ['A', 'B', 'A'], 'type2': ['A', 'A', 'A']},
        {'type1': ['A', 'A', 'B'], 'type2': ['A', 'A', 'A']},
        {'type1': ['A', 'A', 'A'], 'type2': ['B', 'A', 'A']},
        {'type1': ['A', 'A', 'A'], 'type2': ['A', 'B', 'A']},
        {'type1': ['A', 'A', 'A'], 'type2': ['A', 'A', 'B']},
        {'type1': ['C', 'A', 'A'], 'type2': ['A', 'A', 'A']},
        {'type1': ['A', 'C', 'A'], 'type2': ['A', 'A', 'A']},
        {'type1': ['A', 'A', 'C'], 'type2': ['A', 'A', 'A']},
        {'type1': ['A', 'A', 'A'], 'type2': ['C', 'A', 'A']},
        {'type1': ['A', 'A', 'A'], 'type2': ['A', 'C', 'A']},
        {'type1': ['A', 'A', 'A'], 'type2': ['A', 'A', 'C']},
    ])


def test_get_neighbors__with_limited_employ_capacity__no_result_violating_capacity():
    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 3),
        shift_types=['type1', 'type2'],
        initial_shifts={'type1': ['A', 'A', 'A'], 'type2': ['A', 'A', 'A']},
        employees=[
            Employee(name='A'),
            Employee(name='B', capacities=['type1']),
        ])

    neighbors = solution.get_neighbors()
    neighbor_shifts = [n.shifts for n in neighbors]

    assert neighbor_shifts == unordered([
        {'type1': ['B', 'A', 'A'], 'type2': ['A', 'A', 'A']},
        {'type1': ['A', 'B', 'A'], 'type2': ['A', 'A', 'A']},
        {'type1': ['A', 'A', 'B'], 'type2': ['A', 'A', 'A']},
    ])


def test_get_neighbors__with_days_off__no_result_violating_days_off():
    solution = SchedulingSolution(
        date_start=date(2022, 11, 1),
        date_end=date(2022, 11, 3),
        shift_types=['type1', 'type2'],
        initial_shifts={'type1': ['A', 'A', 'A'], 'type2': ['A', 'A', 'A']},
        employees=[
            Employee(name='A'),
            Employee(name='B', days_off=[date(2022, 11, 2), date(2022, 11, 3)]),
        ])

    neighbors = solution.get_neighbors()
    neighbor_shifts = [n.shifts for n in neighbors]

    assert neighbor_shifts == unordered([
        {'type1': ['B', 'A', 'A'], 'type2': ['A', 'A', 'A']},
        {'type1': ['A', 'A', 'A'], 'type2': ['B', 'A', 'A']},
    ])


@pytest.mark.parametrize("left_shift,right_shift,expected", [
    ({'type1': ['A', 'A'], 'type2': ['B', 'B']}, {'type1': ['A', 'A'], 'type2': ['B', 'B']}, True),
    ({'type1': ['A', 'A'], 'type2': ['B', 'B']}, {'type1': ['A', 'A'], 'type2': ['B', 'A']}, False),
])
def test_solution_equal__different_shifts__equal_when_shifts_are_the_same(left_shift, right_shift, expected):
    def get_solution_with_initial_shift(shift):
        return SchedulingSolution(
            date_start=date(2022, 11, 1),
            date_end=date(2022, 11, 2),
            shift_types=['type1', 'type2'],
            initial_shifts=shift,
            employees=[Employee(name='A'), Employee(name='B')])

    left = get_solution_with_initial_shift(left_shift)
    right = get_solution_with_initial_shift(right_shift)

    assert left.__eq__(right) == expected
