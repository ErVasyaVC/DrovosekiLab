import numpy as np
from scipy.optimize import linear_sum_assignment


class Matrix:
    def __init__(self):
        self.n = 15
        self.m = 3000
        self.days_total = 100
        self.v = 7
        self.num_experiments = 50

        self.a_min = 0.12
        self.a_max = 0.22

        self.b_1 = 0.85
        self.b_2 = 1
        self.b_max = 1.15

        self.K_min = 4.8
        self.K_max = 7.05

        self.Na_min = 0.21
        self.Na_max = 0.82

        self.N_min = 1.58
        self.N_max = 2.8

        self.I_min = 0.62
        self.I_max = 0.64

        self.ripening = False
        self.sugar_loss_enabled = False

        self.day_per_stage = round(self.days_total / self.n)
        self.matrix = np.zeros((self.n, self.n))

    def update(self):
        self.day_per_stage = round(self.days_total / self.n)
        self.matrix = np.zeros((self.n, self.n))

    def generate_matrix_b(self):
        matrix_b = np.zeros((self.n, self.n - 1))
        if self.ripening:
            for j in range(self.v - 1):
                matrix_b[:, j] = np.random.uniform(1 + 1e-10, self.b_max, self.n)
            for j in range(self.v - 1, self.n - 1):
                matrix_b[:, j] = np.random.uniform(self.b_1, self.b_2 + 1e-10, self.n)
        else:
            for j in range(self.n - 1):
                matrix_b[:, j] = np.random.uniform(self.b_1, self.b_2 + 1e-10, self.n)
        return matrix_b

    def generate_matrix_i(self):
        matrix_i = np.zeros((self.n, self.n))
        matrix_i[:, 0] = np.random.uniform(self.I_min, self.I_max + 1e-10, self.n)
        for j in range(1, self.n):
            matrix_i[:, j] = matrix_i[:, 0] * (1.029 ** (self.day_per_stage * j))
        return matrix_i

    def generate_matrix_l(self, matrix_i):
        matrix_l = np.zeros((self.n, self.n))
        if self.sugar_loss_enabled:
            k = np.random.uniform(self.K_min, self.K_max + 1e-10, self.n)
            na = np.random.uniform(self.Na_min, self.Na_max + 1e-10, self.n)
            n = np.random.uniform(self.N_min, self.N_max + 1e-10, self.n)
            for i in range(self.n):
                for j in range(self.n):
                    matrix_l[i, j] = (
                        0.1541 * (k[i] + na[i])
                        + 0.2159 * n[i]
                        + 0.9989 * matrix_i[i, j]
                        + 0.1967
                    )
            matrix_l += 1.1
            matrix_l /= 100

        return matrix_l

    def generate_matrix_c(self, matrix_b):
        matrix_c = np.zeros((self.n, self.n))
        matrix_c[:, 0] = np.random.uniform(self.a_min, self.a_max + 1e-10, self.n)
        for i in range(self.n):
            for j in range(1, self.n):
                matrix_c[i, j] = matrix_c[i, j - 1] * matrix_b[i, j - 1]
        return matrix_c

    def generate_all(self):
        self.update()
        matrix_b = self.generate_matrix_b()
        matrix_i = self.generate_matrix_i()
        matrix_l = self.generate_matrix_l(matrix_i)
        matrix_c = self.generate_matrix_c(matrix_b)

        self.matrix = np.maximum(matrix_c - matrix_l, 0)

    def run_algorithms(self):
        strategies = {
            "Максимальная": self.algorithm_maximum,
            "Жадная": self.algorithm_greedy,
            "Бережливая": self.algorithm_thrifty,
            "Жадная/Бережливая": self.algorithm_greedy_thrifty,
            "Бережливая/Жадная": self.algorithm_thrifty_greedy,
        }

        results = {name: [] for name in strategies.keys()}
        cumulative_results = {name: np.zeros(self.n) for name in strategies.keys()}

        for exp in range(self.num_experiments):
            self.generate_all()
            max_result, max_order = self.algorithm_maximum()

            for name, strategy in strategies.items():
                if name == "Максимальная":
                    result, order = max_result, max_order
                else:
                    result, order = strategy()

                results[name].append((result, order))

                cumulative = 0
                if name != "Максимальная":
                    for step, party in enumerate(order):
                        cumulative += self.matrix[party, step]
                        cumulative_results[name][step] += cumulative
                else:
                    for step in range(self.n):
                        cumulative += self.matrix[max_order[step], step]
                        cumulative_results[name][step] += cumulative

        for name in cumulative_results.keys():
            cumulative_results[name] /= self.num_experiments

        avg_results = {}
        relative_losses = {}

        for name in strategies.keys():
            avg_results[name] = np.mean([res[0] for res in results[name]])
            if name != "Максимальная":
                relative_losses[name] = (
                    (avg_results["Максимальная"] - avg_results[name])
                    / avg_results["Максимальная"]
                    * 100
                )
            else:
                relative_losses[name] = 0

        return avg_results, relative_losses, cumulative_results, results

    def algorithm_greedy(self):
        total = 0
        used = set()
        order = []
        for j in range(self.n):
            max_val = 0
            num_max_val = -1
            for i in range(self.n):
                if max_val < self.matrix[i, j] and i not in used:
                    max_val = self.matrix[i, j]
                    num_max_val = i
            used.add(num_max_val)
            order.append(num_max_val)
            total += float(max_val)

        total = round(total * self.day_per_stage * self.m, 4)

        return total, order

    def algorithm_thrifty(self):
        total = 0
        used = set()
        order = []
        for j in range(self.n):
            min_val = 100
            num_min_val = 0
            for i in range(self.n):
                if min_val > self.matrix[i, j] and i not in used:
                    min_val = self.matrix[i, j]
                    num_min_val = i
            used.add(num_min_val)
            order.append(num_min_val)
            total += float(min_val)

        total = round(total * self.day_per_stage * self.m, 4)

        return total, order

    def algorithm_thrifty_greedy(self):
        total = 0
        used = set()
        order = []

        for stage in range(self.v):
            min_value = float("inf")
            best_party = -1

            for party in range(self.n):
                if party not in used:
                    value = self.matrix[party, stage]
                    if value < min_value:
                        min_value = value
                        best_party = party

            used.add(best_party)
            order.append(best_party)
            total += min_value

        for stage in range(self.v, self.n):
            max_value = -1
            best_party = -1

            for party in range(self.n):
                if party not in used:
                    value = self.matrix[party, stage]
                    if value > max_value:
                        max_value = value
                        best_party = party

            used.add(best_party)
            order.append(best_party)
            total += max_value
        total = round(total * self.day_per_stage * self.m, 4)

        return total, order

    def algorithm_greedy_thrifty(self):
        total = 0
        used = set()
        order = []

        for stage in range(self.v):
            max_value = -1
            best_party = -1

            for party in range(self.n):
                if party not in used:
                    value = self.matrix[party, stage]
                    if value > max_value:
                        max_value = value
                        best_party = party

            used.add(best_party)
            order.append(best_party)
            total += max_value

        for stage in range(self.v, self.n):
            min_value = float("inf")
            best_party = -1

            for party in range(self.n):
                if party not in used:
                    value = self.matrix[party, stage]
                    if value < min_value:
                        min_value = value
                        best_party = party

            used.add(best_party)
            order.append(best_party)
            total += min_value

        total = round(total * self.day_per_stage * self.m, 4)

        return total, order

    def algorithm_maximum(self):
        rows, cols = linear_sum_assignment(-self.matrix)

        order = [0] * self.n
        for i in range(self.n):
            order[cols[i]] = int(rows[i])

        total = float(self.matrix[rows, cols].sum())
        total = round(total * self.day_per_stage * self.m, 4)

        return total, order
