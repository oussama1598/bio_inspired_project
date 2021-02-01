import copy

import numpy as np


def roulette_wheel_selection(p):
    c = np.cumsum(p)
    r = sum(p) * np.random.rand()
    ind = np.argwhere(r <= c)
    return ind[0][0]


class DNA:
    def __init__(self, variables, cost):
        self.variables = variables
        self.cost = cost


class GeneticAlgorithm:
    def __init__(self, **kwargs):
        # Problem Definition
        self.const_function = kwargs['cost_function']
        self.variables_min_range = kwargs['variables_min_range']
        self.variables_max_range = kwargs['variables_max_range']

        # Parameters
        self.max_iterations = kwargs['max_iterations']
        self.population = kwargs['population']
        self.beta = kwargs['beta']
        self.pc = kwargs['pc']
        self.gamma = kwargs['gamma']
        self.mutation_rate = kwargs['mutation_rate']
        self.sigma = kwargs['sigma']

        self.nc = int(np.round(self.pc * self.population / 2) * 2)

        self.cost_history = []

    def crossover(self, parent_1: DNA, parent_2: DNA):
        child_1 = copy.deepcopy(parent_1)
        child_2 = copy.deepcopy(parent_2)

        alpha = np.random.uniform(-self.gamma, 1 + self.gamma, *child_1.variables.shape)

        child_1.variables = alpha * parent_1.variables + (1 - alpha) * parent_2.variables
        child_2.variables = alpha * parent_2.variables + (1 - alpha) * parent_1.variables

        return child_1, child_2

    def mutate(self, x):
        y = copy.deepcopy(x)

        flag = np.random.rand(*x.variables.shape) <= self.mutation_rate
        ind = np.argwhere(flag)
        y.variables[ind] += self.sigma * np.random.randn(*ind.shape)

        return y

    def apply_bound(self, x):
        x.variables = np.maximum(x.variables, self.variables_min_range)
        x.variables = np.minimum(x.variables, self.variables_max_range)

    def run(self):
        best_solution = DNA(None, None)
        best_solution.cost = np.inf

        # Initialize Population
        population = []

        for i in range(self.population):
            random_variables = np.random.uniform(
                self.variables_min_range,
                self.variables_max_range,
                len(self.variables_min_range)
            )
            dna_cost = self.const_function(
                random_variables
            )

            dna = DNA(
                random_variables,
                dna_cost
            )

            population.append(dna)

            if dna.cost < best_solution.cost:
                best_solution = copy.deepcopy(dna)

        self.cost_history = []

        for it in range(self.max_iterations):
            costs = np.array([x.cost for x in population])

            avg_cost = np.mean(costs)

            if avg_cost != 0:
                costs = costs / avg_cost

            probs = np.exp(-self.beta * costs)

            children_population = []

            for _ in range(self.nc // 2):
                # Perform Roulette Wheel Selection
                parent_1 = population[roulette_wheel_selection(probs)]
                parent_2 = population[roulette_wheel_selection(probs)]

                # Perform Crossover
                child_1, child_2 = self.crossover(parent_1, parent_2)

                # Perform Mutation
                child_1 = self.mutate(child_1)
                child_2 = self.mutate(child_2)

                # Apply Bounds
                self.apply_bound(child_1)
                self.apply_bound(child_2)

                # Evaluate First Offspring
                child_1.cost = self.const_function(child_1.variables)

                if child_1.cost < best_solution.cost:
                    best_solution = copy.deepcopy(child_1)

                # Evaluate Second Offspring
                child_2.cost = self.const_function(child_2.variables)

                if child_2.cost < best_solution.cost:
                    best_solution = copy.deepcopy(child_2)

                # Add Offsprings to popc
                children_population.append(child_1)
                children_population.append(child_2)

            # Merge, Sort and Select
            population += children_population
            population = sorted(population, key=lambda x: x.cost)
            population = population[0:self.population]

            # Store Best Cost
            self.cost_history.append(best_solution.cost)

        return best_solution
