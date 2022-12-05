from datetime import date
from typing import List

import numpy as np

class Employee:
    def __init__(self, shift: np.ndarray):
        self.shift = shift.astype(int)

class SchedulingSolution:
    def __init__(self, date_start: date, date_end: date, employees: List[Employee]=[]):
        self.date_start = date_start
        self.date_end = date_end
        self.employees = employees

    def fitness(self):
        days = (self.date_end - self.date_start).days + 1
        coverage = np.zeros(days).astype(int)
        for e in self.employees:
            coverage = np.bitwise_or(coverage, e.shift)

        return (sum(coverage) - days) * 10000

    def get_neighbor(self):
        pass
