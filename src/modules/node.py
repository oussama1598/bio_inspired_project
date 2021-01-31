class Node:
    def __init__(self, index, x, y, ddl, force):
        self.index = index
        self.x = float(x)
        self.y = float(y)
        self.ddl = int(ddl)
        self.force = [float(x) for x in force]

        self.u = 0
        self.v = 0

        self._parse_ddl()

    def _parse_ddl(self):
        if self.ddl == 1:
            self.u = 1

        if self.ddl == 2:
            self.v = 1

        if self.ddl == 3:
            self.u = self.v = 1

    def get_u(self):
        return self.index * 2

    def get_v(self):
        return self.get_u() + 1
