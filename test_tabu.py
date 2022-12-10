from tabu import Tabu


def test_no_neighbor():
    tabu = Tabu()
    initial_state = FakeSolution(1)

    result = tabu.solve(initial_state)

    assert result == initial_state


def test_simple_case():
    tabu = Tabu()
    initial_state = FakeSolution(1)
    initial_state.add_neighbor(FakeSolution(3))
    temp = FakeSolution(2)
    temp.add_neighbor(FakeSolution(4))
    initial_state.add_neighbor(temp)

    result = tabu.solve(initial_state)

    assert result == FakeSolution(4)


class FakeSolution:
    def __init__(self, score):
        self.score = score
        self.neighbors = []

    def fitness(self):
        return self.score

    def add_neighbor(self, other):
        self.neighbors.append(other)
        other.neighbors.append(self)

    def get_neighbors(self):
        return self.neighbors

    def __eq__(self, other):
        return self.score == other.score

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(f'score {self.score}')

    def __repr__(self):
        return self.__str__()
