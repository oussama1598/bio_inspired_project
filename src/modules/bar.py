import numpy as np


class Bar:
    def __init__(self, x, y, x1, y1, nodes):
        self.from_x = float(x)
        self.from_y = float(y)
        self.to_x = float(x1)
        self.to_y = float(y1)

        self.nodes = nodes

    def get_length(self):
        return np.sqrt(
            (self.to_x - self.from_x) ** 2 + (self.to_y - self.from_y) ** 2
        )

    def calculate_n(self, length):
        return (1 / length) * np.array([self.to_x - self.from_x, self.to_y - self.from_y])

    def calculate_thermal_force(self, E, A, alpha, delta_t):
        from_node = self.nodes[(self.from_x, self.from_y)]
        to_node = self.nodes[(self.to_x, self.to_y)]

        length = self.get_length()
        unite_vector = self.calculate_n(length)

        print(unite_vector[0])

        n_vector = np.array([[
            -unite_vector[0],
            -unite_vector[1],
            unite_vector[0],
            unite_vector[1]
        ]]).T

        Ks = []

        for node in self.nodes.values():
            if node.index == to_node.index:
                Ks.insert(
                    node.index,
                    [n_vector[:2, :]]
                )
                continue

            if node.index == from_node.index:
                Ks.insert(
                    node.index,
                    [n_vector[2:, :]]
                )

                continue

            Ks.insert(node.index, [np.zeros((2, 1))])

        return np.block(Ks)

    def calculate_k(self, E, A):
        from_node = self.nodes[(self.from_x, self.from_y)]
        to_node = self.nodes[(self.to_x, self.to_y)]

        length = self.get_length()
        unite_vector = self.calculate_n(length)

        n_vector = np.array([[
            -unite_vector[0],
            -unite_vector[1],
            unite_vector[0],
            unite_vector[1]
        ]]).T

        k = ((E * A) / length) * (n_vector * n_vector.T)

        number_of_nodes = len(self.nodes.values())
        Ks = []

        for node in self.nodes.values():
            if node.index == to_node.index:
                Ks.insert(
                    node.index,
                    k[:, :2]
                )
                continue

            if node.index == from_node.index:
                Ks.insert(
                    node.index,
                    k[:, 2:]
                )

                continue

            Ks.insert(node.index, np.zeros((4, 2)))

        k = np.block(Ks)
        Ks = []

        for node in self.nodes.values():
            if node.index == to_node.index:
                Ks.insert(
                    node.index,
                    [k[:2, :]]
                )
                continue

            if node.index == from_node.index:
                Ks.insert(
                    node.index,
                    [k[2:, :]]
                )

                continue

            Ks.insert(node.index, [np.zeros((2, number_of_nodes * 2))])

        return np.block(Ks)
