from src.modules.strcture import Structure

E = 200000
A = 100

structure = Structure.from_csv('./structures/data3.csv')
structure.draw()

print(structure.calculate_displacements(E, A))
