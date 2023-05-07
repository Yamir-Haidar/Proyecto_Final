import base64
import binascii
import os
from collections import deque
from logic.Edge import Edge
from logic.Node import Node
from logic.UnreliableGraph import UnreliableGraph


class Graph:

    def __init__(self):
        self.nodes = deque()

    def insert_node(self, info) -> bool:
        """
                Inserta un nodo al grafo dada su info

                :param info: La info del nodo
                :return: (True) En caso de insertar el nodo
                :return: (False) En caso de no poder insertar el nodo dado que ya existia
                """
        exists = False
        if self.existing_node(info):
            exists = True
        else:
            node = Node(info)
            self.nodes.append(node)
        return not exists

    def insert_edge(self, info1, info2, weight=1) -> bool:
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
        success = False
        node1 = self.get_node(info1)
        if node1 is not None:
            node2 = self.get_node(info2)
            if node2 is not None:
                if node2 not in node1.get_adjacent():
                    edge = Edge(node2, weight)
                    node1.insert_edge(edge)
                    success = True
        return success

    def update_node(self, old_info, new_info) -> bool:
        """
            Actualiza un nodo dada su info

            :param old_info: Info actual del nodo
            :param new_info: Info con la que se va a actualizar el nodo
            :return: (True) En caso de que pudo actualizar el nodo
            :return: (False)  En caso de que no pudo actualizar el nodo dado que no existe
        """
        updated = False
        node = self.get_node(old_info)
        if node is not None:
            if not self.existing_node(new_info):
                node.info = new_info
                updated = True
        return updated

    def update_edge(self, info1, info2, weight: int) -> bool:
        """
             Actualiza el peso una arista comprendida entre dos nodos

             :param info1: Info del nodo que sale la arista
             :param info2: Info del nodo al que apunta la arista
             :param weight: Peso de la arista
             :return: (True) En caso de que pudo actualizar el peso de la arista
             :return: (False) En caso de que no pudo actualizar el peso de la
             arista dado que no existe alguno de los nodos o la arista
        """
        updated = False
        edge = self.get_edge(info1, info2)
        if edge is not None:
            edge.weight = weight
            updated = True
        return updated

    def delete_node(self, info) -> bool:
        """
            Elimina un nodo dada su info

            :param info: Info del nodo
            :return: (True) En caso de que pudo eliminar el nodo
            :return: (False)  En caso de que no pudo eliminar el nodo dado que no existe
        """
        deleted = False
        node_to_delete = self.get_node(info)
        if node_to_delete is not None:
            it = iter(self.nodes)
            while True:
                try:
                    node = next(it)
                    self.delete_edge(node.get_info(), info)
                except StopIteration:
                    break
            self.nodes.remove(node_to_delete)
            deleted = True
        return deleted

    def delete_edge(self, info1, info2) -> bool:
        """
            Elimina una arista comprendida entre dos nodos

            :param info1: Info del nodo que sale la arista
            :param info2: Info del nodo al que apunta la arista
            :return: (True) En caso de que pudo eliminar la arista
            :return: (False) En caso de que no pudo eliminar la arista dado
            que no existe alguno de los nodos o la arista
        """
        deleted = False
        edge = self.get_edge(info1, info2)
        if edge is not None:
            node1 = self.get_node(info1)
            node1.delete_edge(edge)
            deleted = True
        return deleted

    def existing_node(self, info) -> bool:
        """
            Indica si existe una nodo dada su info

            :param info: Info del nodo
            :return: (True) En caso de que exista el nodo
            :return: (False)  En caso de que no exista el nodo
         """
        exists = False
        if self.get_node(info) is not None:
            exists = True
        return exists

    def existing_edge(self, info1, info2) -> bool:
        """
            Indica si existe una arista comprendida entre dos nodos

            :param info1: Info del nodo que sale la arista
            :param info2: Info del nodo al que apunta la arista
            :return: (True) En caso de que exista la arista y los nodos
            :return: (False) En caso de no existir la arista o alguno de los nodos
         """
        exists = False
        edge: Edge = self.get_edge(info1, info2)
        if edge is not None:
            exists = True
        return exists

    def get_edge(self, info1, info2) -> Edge:
        """
            Retorna una arista comprendida entre dos nodos

            :param info1: Info del nodo que sale la arista
            :param info2: Info del nodo al que apunta la arista
            :return: (None) En caso de no existir la arista o alguno de los nodos
        """
        node1 = self.get_node(info1)
        edge = node1.get_edge(info2)
        return edge if node1 is not None and self.existing_node(info2) else None

    def get_node(self, info) -> Node:
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

    def breadth_first_search(self, inicio) -> list:
        """
        Realiza un recorrido a lo ancho(bfs)
        :param inicio: Nodo inicial del recorrido
        :return: lista de nodos que recorre en su ejecucion
        """
        visited = []
        queue = deque()
        for node in self.nodes:
            if node.info == inicio:
                queue.append(node)

        while queue:
            current_node = queue.popleft()
            visited.append(current_node)

            for edge in current_node.edges:
                if edge.node not in visited and edge.node not in queue:
                    queue.append(edge.node)
        return visited

    def depth_first_search(self, start: str) -> list:
        """
        Realiza un recorrido en profundidad(dfs)
        :param start: Nodo inicial del recorrido
        :return: lista de nodos que recorre en su ejecucion
        """
        visited = []
        start = self.get_node(start)
        self._depth_first_search(start, visited)
        return visited

    def _depth_first_search(self, node, visited) -> None:
        """
        Funcion auxiliar de depth_first_search
        :param node: Nodo actual
        :param visited: lista con los nodos visitados
        :return:
        """
        visited.append(node)
        for edge in node.edges:
            if edge.node not in visited:
                self._depth_first_search(edge.node, visited)

    def save(self, filename: str) -> None:
        """
        Funcion que permite guardar el fichero en la raiz del proyecto
        :param filename: Nombre del fichero
        :return: None
        """
        with open("../" + filename + ".txt", 'w') as file:
            for node in self.nodes:
                file.write(node.info + " ")
                for edge in node.edges:
                    file.write(f"({edge.node}-{edge.weight})")
                file.write("\n")

    @staticmethod
    def load(filename) -> 'Graph':
        """
        Devuelve un grafo luego de cargarlo de un fichero
        :param filename: Nombre del fichero
        :return: Graph
        """

        with open("../" + filename + ".txt", "r", encoding="utf-8") as file:
            graph = Graph()
            dicts = {}
            for line in file:
                data = list(line.replace("(", " ").replace(")", " ").replace("-", "  ").strip("  ").split())
                graph.insert_node(str(data[0]))
                node = graph.get_node(data[0])
                dicts[node.info] = data[1:len(data)]
            for key in dicts:
                for i in range(0, len(dicts[key]), 2):
                    if graph.get_node(dicts[key][i]) in graph.nodes:
                        if Edge(dicts[key][i], dicts[key][i + 1]) in graph.get_node(key).edges:
                            raise Exception(f"Ya existe la arista {graph.get_node(key)} ->"
                                            f" {dicts[key][i]} con peso {dicts[key][i + 1]}")
                        else:
                            graph.get_node(key).insert_edge(Edge(dicts[key][i], dicts[key][i + 1]))
                    else:
                        raise Exception(f"El nodo {dicts[key][i]} no pertenece al grafo")
        return graph

    def export_graph(self, filename: str):
        """
        Exporta un grafo a un archivo txt
        :param filename: El nombre del archivo de texto
        :return:
        """
        os.makedirs("../", exist_ok=True)
        with open("../" + filename + ".txt", 'w') as file:
            file.write(base64.b64encode("python_project directed_graph".encode("utf-8")).decode('utf-8'))
            file.write('\n')
            it = iter(self.nodes)
            while True:
                try:
                    starting_node = next(it)
                    line: str
                    line = "".join([starting_node.info])
                    it2 = iter(starting_node.edges)
                    while True:
                        try:
                            edge = next(it2)
                            node_adjacent = edge.node
                            line = "".join([line, " , ", str(edge.weight), " , ", node_adjacent.info])
                        except StopIteration:
                            file.write(f"{base64.b64encode(line.encode('utf-8')).decode('utf-8')}\n")
                            break
                except StopIteration:
                    break
        os.chmod("../" + filename + ".txt", 0o444)

    @staticmethod
    def import_graph(filename: str):

        """
        Importa un grafo (exportado a un fichero texto previamente) dado su direccion y nombre
        -En caso de no encontrarse el fichero en la direccion y nombre especificados lanzara la excepcion
        FileNotFoundError
        -En caso de importar un fichero que no haya sido exportado por el metodo export_graph() o que no contenga la
        estructura definida lanzara la excepcion UnreliableGraph que indica que el grafo que se desea importar no
        es confiable
        :param filename: El nombre del archivo de texto
        :return:
        """
        graph = Graph()
        try:
            with open("../" + filename + ".txt", 'r') as file:
                flag = True
                line = file.readline()
                decode_line = base64.b64decode(line).decode('utf-8')
                if decode_line == "python_project directed_graph":
                    while line:
                        line = file.readline()
                        decode_line = base64.b64decode(line).decode('utf-8')
                        info: deque = deque(decode_line.split(" , "))
                        it = iter(info)
                        starting_node: str
                        while True:
                            try:
                                if flag:
                                    starting_node = next(it)
                                    graph.insert_node(starting_node)
                                    flag = False
                                else:
                                    im = next(it)
                                    weight = int(im)
                                    adjacent_node = next(it)
                                    graph.insert_node(adjacent_node)
                                    graph.insert_edge(starting_node, adjacent_node, weight)
                            except StopIteration:
                                flag = True
                                break
        except binascii.Error:
            raise UnreliableGraph
        except FileNotFoundError:
            raise FileNotFoundError
