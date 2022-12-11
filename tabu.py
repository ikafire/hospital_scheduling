def better_than(sol1, sol2):
    if not sol2:
        return sol1
    else:
        return sol1.fitness() > sol2.fitness()


class Tabu:
    def __init__(self):
        self.max_iter = 100

    def solve(self, solution):
        best = solution
        current = solution
        tabu_list = []
        tabu_list.append(best)

        i = 0
        while i < self.max_iter:
            neighbors = current.get_neighbors()
            if not neighbors:
                break

            best_non_tabu_neighbor = None
            best_neighbor = None
            for neighbor in neighbors:
                if better_than(neighbor, best_neighbor):
                    best_neighbor = neighbor
                if (neighbor not in tabu_list) and better_than(neighbor, best_non_tabu_neighbor):
                    best_non_tabu_neighbor = neighbor

            # ignore tabu rule if nowhere to go
            if best_non_tabu_neighbor:
                current = best_non_tabu_neighbor
            else:
                current = best_neighbor

            if current.fitness() > best.fitness():
                best = current

            if current not in tabu_list:
                tabu_list.append(current)

            print(f'best: {best}, fitness {best.fitness()}')
            # print(f'current: {current}, fitness {current.fitness()}')
            # print(f'tabu: {len(tabu_list)}')

            i = i + 1

        return best
