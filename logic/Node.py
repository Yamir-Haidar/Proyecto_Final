import re

from logic import Edge


class Node:
    def __init__(self, info: str):
        if re.match(r'^[a-zA-Z0-9]+$', info) is None:
            raise Exception(f"Invalid name {info}")
        self.info = info
        self.edges = []

    def __str__(self):
        return self.info

    def __eq__(self, other) -> bool:
        return self.info == other.info if type(other) is not str else False

    def get_edge(self, info) -> Edge:
        it = iter(self.edges)
        while it:
            try:
                aux = next(it)
                node = aux.node
                if node.info == info:
                    return aux
            except StopIteration:
                break
        return info

    def get_adjacent(self) -> list:
        adjacent = []
        it = iter(self.edges)
        while it:
            try:
                edge = next(it)
                if edge.node not in adjacent:
                    adjacent.append(edge.node)
            except StopIteration:
                break
        return adjacent

    def update_edge(self, end, weight: int) -> None:
        edge = self.get_edge(end)
        if edge is not None:
            edge.weight = weight
        else:
            raise Exception(f"Edge {self.info} -> {end} not exists")

    def insert_edge(self, edge: Edge) -> None:
        if edge in self.edges:
            raise Exception(f"Edge {self.info} -> {edge.node.info} already exists")
        else:
            self.edges.append(edge)

    def delete_edge(self, edge: Edge):
        try:
            self.edges.remove(edge)
        except ValueError:
            raise Exception(f"Edge {self.info} -> {edge.node if type(edge) is not str else edge} unfounded")
