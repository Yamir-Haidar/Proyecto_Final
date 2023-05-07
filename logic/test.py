from Graph import Graph

grafo = Graph()

grafo.insert_node("A")
grafo.insert_node("B")
grafo.insert_node("C")
grafo.insert_node("D")
# grafo.insert_node("E")
grafo.insert_edge("A", "B")
grafo.insert_edge("A", "B")

grafo.insert_edge("A", "C")
# grafo.insert_edge("A", "E")
grafo.insert_edge("B", "D")
grafo.insert_edge("C", "D")
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
grafo = Graph.import_graph("pan")
for item in grafo.nodes:
    print(item, end=" ")
    for edge in item.edges:
        print(edge, end=" ")
    print()
