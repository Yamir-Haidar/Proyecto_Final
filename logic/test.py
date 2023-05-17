from Graph import Graph

grafo = Graph()


def print_dic(dic: dict):
    for key, values in dic.items():
        print(key)
        for value in values:
            print(value)


grafo.insert_node("A")
grafo.insert_node("B")

grafo.insert_edge("A", "A")
grafo.insert_edge("A", "B")
grafo.update_edge("B", "B")
grafo.delete_node("A")
# grafo.insert_node("B")
# grafo.insert_node("C")
# grafo.insert_node("D")
# grafo.insert_edge("A", "B", 1)
# grafo.update_edge("A", "x", 2)
# grafo.delete_edge("A", "C")
# print_dic(grafo.get_nodes_and_edges())
# grafo.delete_node("B")
# print_dic(grafo.get_nodes_and_edges())

# grafo.insert_node("E")
# grafo.insert_edge("A", "B")
# grafo.update_edge("A", "B", "C")
# grafo.delete_edge("A", "B", 1)
# grafo.insert_edge("A", "B")

# grafo.insert_edge("A", "C")
# grafo.insert_edge("A", "E")
# grafo.insert_edge("B", "D")
# grafo.insert_edge("C", "D")
# grafo.insert_edge("D", "C")
# grafo.insert_edge("C", "D")
# for node in grafo.depth_first_search("A"):
#     print(node)
# for i in grafo.get_node("A").get_adjacent():
#     print(i)
# grafo.save("plastilina")
# grafo.save("test")
# grafo = Graph.load("test")
# grafo.export_graph("pan")
# grafo = Graph.import_graph("pan")
# for item in grafo.nodes:
#     print(item, end=" ")
#     for edge in item.edges:
#         print(edge, end=" ")
#     print()
