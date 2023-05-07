from logic import Node


class Edge:

    def __init__(self, node: Node, weight=1):
        self.node = node
        self.weight = weight

    def __str__(self):
        return f"{self.node},{self.weight}"

    def __eq__(self, other):
        return self.node == other.node and self.weight == other.weight
