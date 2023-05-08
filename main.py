from logic.Graph import Graph
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

graph = Graph()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_nodes")
async def get_nodes():
    return graph.get_nodes_and_edges()


@app.post("/insert_node")
async def insert_node(info: str):
    return graph.insert_node(info)


@app.post("/insert_edge")
async def insert_edge(start: str, end: str, weight=1):
    return graph.insert_edge(start, end, weight)


@app.post("/update_node")
async def update_node(old_info: str, new_info: str):
    return graph.update_node(old_info, new_info)


@app.post("/update_edge")
async def update_edge(start: str, old_end: str, new_end: str, old_weight=1, new_weight=1):
    return graph.update_edge(start, old_end, new_end, old_weight, new_weight)


@app.delete("/delete_node")
async def delete_node(info: str):
    return graph.delete_node(info)


@app.delete("/delete_edge")
async def delete_edge(start: str, end: str, weight=1):
    return graph.delete_edge(start, end, weight)


@app.get("/bfs")
async def breadth_first_search(start: str) -> list:
    return graph.breadth_first_search(start)


@app.get("/dfs")
async def depth_first_search(start: str):
    return graph.depth_first_search(start)


@app.post("/save")
async def save(filename: str):
    return graph.save(filename)


@app.get("/load")
async def load(filename: str):
    return graph.load(filename)


@app.post("/export")
async def export_graph(filename: str):
    return graph.export_graph(filename)


@app.get("/import")
async def import_graph(filename: str):
    return graph.import_graph(filename)
