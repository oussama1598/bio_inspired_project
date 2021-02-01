from src.modules.strcture import Structure
import matplotlib.pyplot as plt
from ypstruct import structure
from src.modules.genetic_algorithm import GeneticAlgorithm

E = 200000
A = 100

bars_structure = Structure.from_csv('structures/example_1.csv')
bars_structure.draw()

print(bars_structure.calculate_displacements(E, A))
print(bars_structure.calculate_deformation_energy(A, E))

def calculate_energy(x):
    return bars_structure.calculate_deformation_energy(x[0], E)


genetic_algorithm = GeneticAlgorithm(
    cost_function=calculate_energy,
    variables_min_range=[0.000000001],
    variables_max_range=[10000],
    max_iterations=100,
    population=50,
    beta=1,
    pc=1,
    gamma=0.1,
    mutation_rate=0.01,
    sigma=0.1
)

best_solution = genetic_algorithm.run()

# Results
plt.plot(genetic_algorithm.cost_history)
plt.xlim(0, genetic_algorithm.max_iterations)
plt.xlabel('Iterations')
plt.ylabel('Best Cost')
plt.title('Genetic Algorithm (GA)')
plt.grid(True)
plt.show()
