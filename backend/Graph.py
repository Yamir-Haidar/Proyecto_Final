import re
from collections import deque
from backend.Edge import Edge
from backend.Node import Node
from backend.utils import is_right


class Graph:

    def __init__(self):
        self.nodes = deque()

    def clear_graph(self):
        self.nodes.clear()

    def get_nodes_and_edges(self):
        result = {"nodes": [], "edges": []}
        for node in self.nodes:
            result["nodes"].append(node.info)
            for edge in node.edges:
                result["edges"].append([node.info, edge.node.info, edge.weight])
        return result

    def insert_node(self, info: str):
        """
                Inserta un nodo al grafo dada su info

                :param info: La info del nodo
                :return: (True) En caso de insertar el nodo
                :return: (False) En caso de no poder insertar el nodo dado que ya existia
                """
        if self.existing_node(info):
            raise Exception(f"Node {info} already exists")
        node = Node(info)
        self.nodes.append(node)

    def insert_edge(self, info1: str, info2: str, weight="1") -> None:
        """
       Inserta una arista entre dos nodos

       :param info1: Info del nodo que sale la arista
       :param info2: Info del nodo al que apunta la arista
       :param weight: Peso de la arista
       :return : (True) En caso de que pudo insertar la arista
              entre ambos nodos
       :return : (False) En caso de que no pudo insertar la arista dado que no existe
       alguno de los nodos o que existia previamente una arista
              entre ambos nodos

       """
        node1 = self.get_node(info1)
        if node1 is None:
            raise Exception(f"Node {info1} not exists")
        node2 = self.get_node(info2)
        if node2 is None:
            raise Exception(f"Node {info2} not exists")
        if not is_right(weight):
            raise Exception("Invalid weight")
        edge = Edge(node2, weight)
        if edge in node1.edges:
            raise Exception(f"Edge {info1} -> {info2} already exists")
        node1.insert_edge(edge)

    def update_node(self, old_info: str, new_info: str) -> None:
        """
            Actualiza un nodo dada su info

            :param old_info: Info actual del nodo
            :param new_info: Info con la que se va a actualizar el nodo
            :return: (True) En caso de que pudo actualizar el nodo
            :return: (False)  En caso de que no pudo actualizar el nodo dado que no existe
        """
        node = self.get_node(old_info)
        if node is None:
            raise Exception(f"Node {old_info} unfounded")
        if self.get_node(old_info) == self.get_node(new_info):
            raise Exception("New info is equal to the previous one")
        if self.existing_node(new_info):
            raise Exception(f"Node {new_info} already exists")
        if re.match(pattern=r'^[a-zA-Z0-9]+$', string=new_info) is None:
            raise Exception(f"Invalid name {new_info}")
        node.info = new_info

    def update_edge(self, start: str, end: str, weight=1):
        node1 = self.get_node(start)
        if node1 is None or node1 not in self.nodes:
            raise Exception(f"Node {start} not exists")
        node2 = self.get_node(end)
        if node2 is None or node2 not in self.nodes:
            raise Exception(f"Node {end} not exists")
        edge = Edge(node2, weight)
        if edge in node1.edges:
            if not is_right(weight):
                raise Exception("Invalid weight")
            elif node1.get_edge(end).weight == weight:
                raise Exception(f"Edge {start} -> {end} with weight {weight} already exists")
            else:
                node1.get_edge(end).weight = weight
        else:
            raise Exception(f"Non existent edge {start} -> {end}")

    def delete_node(self, info: str) -> None:
        """
            Elimina un nodo dada su info

            :param info: Info del nodo
            :return: (True) En caso de que pudo eliminar el nodo
            :return: (False)  En caso de que no pudo eliminar el nodo dado que no existe
        """
        node_to_delete = self.get_node(info)
        if node_to_delete is None:
            raise Exception(f"Node {info} not exists")
        it = iter(self.nodes)
        while it:
            try:
                node = next(it)
                for edge in node.edges:
                    if node_to_delete.info == edge.node.info:
                        node.delete_edge(node.get_edge(info))
            except StopIteration:
                break
        self.nodes.remove(node_to_delete)

    def delete_edge(self, start: str, end: str):
        node1 = self.get_node(start)
        if node1 not in self.nodes:
            raise Exception(f"Node {start} not exists")
        node2 = self.get_node(end)
        if node2 not in self.nodes:
            raise Exception(f"Node {end} not exists")
        node1.delete_edge(node1.get_edge(end))

    def existing_node(self, info: str) -> bool:
        """
            Indica si existe un nodo dada su info

            :param info: Info del nodo
            :return: (True) En caso de que exista el nodo
            :return: (False)  En caso de que no exista el nodo
         """
        return self.get_node(info) is not None

    def get_node(self, info: str) -> Node:
        """
            Retorna un nodo dada su info

            :param info: Info del nodo
            :return: (None) En caso de que no exista el nodo
        """
        node = None
        it = iter(self.nodes)
        while True:
            try:
                aux = next(it)
                if aux.info == info:
                    node = aux
                    break
            except StopIteration:
                break
        return node

    def breadth_first_traversal(self, start: str) -> list:
        """
        Realiza un recorrido a lo ancho(bfs)
        :param start: Nodo inicial del recorrido
        :return: lista de nodos que recorre en su ejecucion
        """
        visited = []
        queue = deque()
        start_node = self.get_node(start)
        if start_node is None:
            raise Exception(f"Node {start} non exists")
        queue.append(start_node.info)

        while queue:
            current_node = self.get_node(queue.popleft())
            visited.append(current_node.info)
            for edge in current_node.edges:
                if edge.node.info not in visited and edge.node.info not in queue:
                    queue.append(edge.node.info)
        return visited

    def depth_first_traversal(self, start: str) -> list:
        """
        Realiza un recorrido en profundidad(dfs)
        :param start: Nodo inicial del recorrido
        :return: lista de nodos que recorre en su ejecucion
        """
        visited = []
        start_node = self.get_node(start)
        if start is None:
            raise Exception(f"Node {start} non exists")
        self._depth_first_search(start_node, visited)
        return visited

    def _depth_first_search(self, node: Node, visited: list) -> None:
        """
        Funcion auxiliar de depth_first_search
        :param node: Nodo actual
        :param visited: lista con los nodos visitados
        :return:
        """
        visited.append(node.info)
        for edge in node.edges:
            if edge.node.info not in visited:
                self._depth_first_search(edge.node, visited)

    def save(self, full_path: str) -> None:
        """
        Funcion que permite guardar el fichero en la raiz del proyecto
        :param full_path: Ruta y nombre del fichero
        :return: None
        """
        with open(full_path, 'w') as file:
            file.write("@iqh2eie39(*\n")
            for node in self.nodes:
                file.write(node.info + " ")
                for edge in node.edges:
                    file.write(f"({edge.node}-{edge.weight})")
                file.write("\n")

    def load(self, str_file: str):
        """
            Devuelve un grafo luego de cargarlo de un fichero
            :param str_file: Archivo en formato str de donde proviene el grafo
            :return: Graph
        """
        lines = str_file.splitlines()
        dicts = {}
        graph = Graph()
        if lines[0] != "@iqh2eie39(*":
            raise Exception("Invalid file")
        try:
            for line in lines[1: len(lines)]:
                if not is_right(line, 1):
                    raise Exception("Invalid sequence: " + line)
                data = list(line.replace("(", " ").replace(")", " ").replace("-", "  ").strip("  ").split())
                graph.insert_node(data[0])
                node = graph.get_node(data[0])
                dicts[node.info] = data[1:len(data)]
            for start_node in dicts:
                for i in range(0, len(dicts[start_node]), 2):
                    end_node = graph.get_node(dicts[start_node][i])
                    weight = str(dicts[start_node][i + 1])
                    if end_node is None:
                        raise Exception(f"Node {dicts[start_node][i]} has not been created")
                    if end_node not in graph.nodes:
                        raise Exception(f"Node {dicts[start_node][i]} doesn't belong to the graph")
                    edge = Edge(end_node, weight)
                    if edge in graph.get_node(start_node).edges:
                        raise Exception(f"Edge {str(start_node)} -> {str(end_node)} "
                                        f"with weight {weight} already exists")
                    else:
                        graph.get_node(start_node).insert_edge(edge)
            self.nodes = graph.nodes
        except Exception as e:
            raise Exception("Error reading file, ", e)
