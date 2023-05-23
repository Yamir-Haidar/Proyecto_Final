from backend import Node


class Edge:

    def __init__(self, node: Node, weight=1):
        self.node = node
        self.weight = weight

    def __str__(self):
        return f"{self.node},{self.weight}"

    def __eq__(self, other: 'Edge'):
        return self.node == other.node if type(other) is Edge else False
