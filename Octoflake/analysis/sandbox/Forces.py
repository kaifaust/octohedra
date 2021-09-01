import math


class OctoNode:

    def __init__(self, level, column, row, connections=None):
        self.level = level
        self.column = column
        self.row = row
        self.connections = connections if connections is not None else set()

    def coordinates(self):
        return f"({self.level}, {self.column}, {self.row})"

    def __str__(self):
        return f"OctoNode{self.coordinates()} {self.connections=}"



class Octoflake:

    def __init__(self):
        self.nodes = {}
        self.edges = {}



    def build(self, iteration):
        assert iteration<2
        edge_length = 2 ** iteration + 1


        for level in range(edge_length):
            for row in range(edge_length):
                for column in range(edge_length):
                    print(level, row, column)








point1 = OctoNode(0, 1, 3)


flake = Octoflake()
flake.build(1)


print(point1)

