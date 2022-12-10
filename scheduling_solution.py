from datetime import date, timedelta
from typing import List, Dict
import copy
import random

import numpy as np


class Employee:
    def __init__(self,
                 name: str,
                 capacities: List[str]=[],
                 days_off: List[date]=[]):
        self.name = name
        self.capacities = capacities
        self.days_off = days_off

    def can_do(self, shift_type: str, date: date):
        if self.capacities and not shift_type in self.capacities:
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

        shift_worker_candidates = {} # Dict[type][day] = list of candidates
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
                    shift[i] = self.shift_worker_candidates[t][i][0]
                self.shifts[t] = shift

    def fitness(self):
        days = (self.date_end - self.date_start).days + 1
        coverage = np.zeros(days).astype(int)
        for e in self.employees:
            coverage = np.bitwise_or(coverage, np.array(e.shift))

        return (sum(coverage) - days) * 10000

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
