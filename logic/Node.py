from logic import Edge


class Node:
    def __init__(self, info):
        self.info = info
        self.edges = []

    def __str__(self):
        return self.info

    def get_edge(self, info) -> Edge:
        edge = None
        it = iter(self.edges)
        while True:
            try:
                aux = next(it)
                node = aux.node
                if node.info == info:
                    edge = aux
                    break
            except StopIteration:
                break
        return edge

    def get_adjacent(self) -> list:
        adjacent = []
        it = iter(self.edges)
        while True:
            try:
                edge = next(it)
                adjacent.append(edge.node)
            except StopIteration:
                break
        return adjacent

    def insert_edge(self, edge: Edge):
        self.edges.append(edge)

    def delete_edge(self, edge: Edge):
        self.edges.remove(edge)
