import csv

import numpy as np
import matplotlib.pyplot as plt

from src.modules.bar import Bar
from src.modules.node import Node


class Structure:
    def __init__(self, structure_config):
        self.structure_config: np.array = np.array(
            structure_config
        )

        self.nodes = {}
        self.bars = {}

        self._parse_bars()

    @classmethod
    def from_csv(cls, file_path: str):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            return cls(list(reader)[1:])

    def _parse_bars(self):
        for i, from_node in enumerate(self.structure_config):
            from_x, from_y = from_node[:2]
            other_nodes = from_node[2:-3]

            from_x = float(from_x)
            from_y = float(from_y)

            if (from_x, from_y) not in self.nodes:
                self.nodes[(from_x, from_y)] = Node(
                    i,
                    from_x,
                    from_y,
                    from_node[-3],
                    [from_node[-2], from_node[-1]]
                )

            for j, link_exists in enumerate(other_nodes):
                if i == j or int(link_exists) == 0:
                    continue

                if frozenset((i, j)) in self.bars:
                    continue

                to_node = self.structure_config[j]
                to_x, to_y = to_node[:2]

                self.bars[frozenset((i, j))] = Bar(
                    from_x,
                    from_y,
                    to_x,
                    to_y,
                    self.nodes
                )

    def calculate_ll_k_with_forces(self, E, A):
        k = np.sum(bar.calculate_k(E, A) for bar in self.bars.values())

        nodes = sorted(list(self.nodes.values()), key=lambda x: x.index)
        axis_indices = []
        forces = []

        for i, node in enumerate(nodes):
            if node.u == 0 and node.v == 0:
                continue

            u_index = node.get_u()
            v_index = node.get_v()

            if node.u:
                axis_indices.append(u_index)
                forces.append(node.force[0])

            if node.v:
                axis_indices.append(v_index)
                forces.append(node.force[1])

        ll_k = []

        for i in axis_indices:
            line = []

            for j in axis_indices:
                line.append(k[i][j])

            ll_k.append(line)

        return np.array(ll_k), np.array([forces]).T, axis_indices

    def calculate_displacements(self, E, A):
        ll_k, forces, displacements_indices = self.calculate_ll_k_with_forces(E, A)

        unknown_displacements = np.linalg.solve(ll_k, forces)
        all_displacements = [0 for _ in range(2 * len(self.nodes.values()))]

        for i, index in enumerate(displacements_indices):
            all_displacements[index] = unknown_displacements[i][0]

        return np.array(all_displacements)

    def calculate_deformation_energy(self, E, A):
        k = np.sum(bar.calculate_k(E, A) for bar in self.bars.values())
        displacements = np.array([self.calculate_displacements(E, A)])

        return (1 / 2) * np.dot(np.dot(displacements, k), displacements.T)[0][0]

    def draw(self, show=True):
        fig, ax = plt.subplots()

        for node in self.nodes.values():
            ax.scatter([node.x], [node.y], color='r',
                       zorder=2,
                       s=120)

        for bar in self.bars.values():
            ax.plot([bar.from_x, bar.to_x], [bar.from_y, bar.to_y], color='b', zorder=1)

        if show:
            fig.show()
