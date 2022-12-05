from datetime import date
from typing import List
import copy
import random
import uuid

import numpy as np

class Employee:
    def __init__(self, shift: List[int], id=None):
        self.shift = shift
        if id:
            self.id = id
        else:
            self.id = uuid.uuid4()

    def get_neighbors(self):
        neighbors = []
        for i in range(len(self.shift)):
            clone = copy.deepcopy(self)
            if clone.shift[i] == 0:
                clone.shift[i] = 1
            else:
                clone.shift[i] = 0
            neighbors.append(clone)

        random.shuffle(neighbors)
        return neighbors

    def __str__(self):
        return f'employee {str(self.id)[:8]}: {"".join(map(str, self.shift))}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id and \
            np.array_equal(self.shift, other.shift)

    def __ne__(self, other):
        return not self.__eq__(other)


class SchedulingSolution:
    def __init__(self, date_start: date, date_end: date, employees: List[Employee]=[]):
        self.date_start = date_start
        self.date_end = date_end
        self.employees = employees

    def fitness(self):
        days = (self.date_end - self.date_start).days + 1
        coverage = np.zeros(days).astype(int)
        for e in self.employees:
            coverage = np.bitwise_or(coverage, np.array(e.shift))

        return (sum(coverage) - days) * 10000

    def get_neighbors(self):
        neighbors = []

        for i, employee in enumerate(self.employees):
            for employee_neighbor in employee.get_neighbors():
                clone = copy.deepcopy(self)
                clone.employees[i] = employee_neighbor
                neighbors.append(clone)

        return neighbors

    def __str__(self):
        lines = []
        for e in self.employees:
            lines.append(str(e))

        return '\n'.join(lines)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.date_start == other.date_start and \
            self.date_end == other.date_end and \
            np.array_equal(self.employees, other.employees)

    def __ne__(self, other):
        return not self.__eq__(other)
