from datetime import date, timedelta
from typing import List, Dict
import copy
import random
from collections import Counter
import itertools


class Employee:
    def __init__(self,
                 name: str,
                 capacities: List[str] = [],
                 days_off: List[date] = []):
        self.name = name
        self.capacities = capacities
        self.days_off = days_off

    def can_do(self, shift_type: str, date: date):
        if self.capacities and shift_type not in self.capacities:
            return False

        if date in self.days_off:
            return False

        return True


class SchedulingSolution:
    def __init__(self,
                 date_start: date,
                 date_end: date,
                 employees: List[Employee],
                 shift_types: List[str],
                 initial_shifts: Dict[str, List[str]] = {}):

        self.date_start = date_start
        self.date_end = date_end
        self.employees = employees
        self.shift_types = shift_types
        self.days = (date_end - date_start).days + 1

        shift_worker_candidates = {}  # Dict[type][day] = list of candidates
        for t in shift_types:
            candidates_of_this_type = []
            for i in range(self.days):
                d = self.date_start + timedelta(days=i)
                candidates = [e.name for e in self.employees if e.can_do(t, d)]
                candidates_of_this_type.append(candidates)
            shift_worker_candidates[t] = candidates_of_this_type
        self.shift_worker_candidates = shift_worker_candidates

        if initial_shifts:
            self.shifts = initial_shifts
        else:
            self.shifts = {}
            for t in shift_types:
                shift = [''] * self.days
                for i in range(self.days):
                    shift[i] = random.choice(self.shift_worker_candidates[t][i])
                self.shifts[t] = shift

    def fitness(self):
        return self.concurrent_shift_penalty() + self.too_many_shifts_penalty()

    def concurrent_shift_penalty(self):
        penalty = 0
        shift_size = len(self.shift_types)
        for workers in zip(*self.shifts.values()):
            unique_workers = len(set(workers))
            concurrent_shifts = shift_size - unique_workers
            penalty = penalty - concurrent_shifts * 100000
        return penalty

    def too_many_shifts_penalty(self):
        penalty = 0
        shifts_per_employee = Counter(itertools.chain(*self.shifts.values()))
        for shift_count in shifts_per_employee.values():
            overshifts = shift_count - 8
            if overshifts > 0:
                penalty = penalty - overshifts * 10000
        return penalty

    def get_neighbors(self):
        neighbors = []

        for t in self.shift_types:
            shift = self.shifts[t]
            for i, shift_worker in enumerate(shift):
                candidates = self.shift_worker_candidates[t][i]
                for candidate in candidates:
                    if candidate != shift_worker:
                        clone = copy.deepcopy(self)
                        clone.shifts[t][i] = candidate
                        neighbors.append(clone)

        random.shuffle(neighbors)
        return neighbors

    def __str__(self):
        lines = []
        for t in self.shift_types:
            lines.append(str(self.shifts[t]))

        return '\n'.join(lines)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.date_start == other.date_start and \
            self.date_end == other.date_end and \
            self.shifts == other.shifts

    def __ne__(self, other):
        return not self.__eq__(other)
