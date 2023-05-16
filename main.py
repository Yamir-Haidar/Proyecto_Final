from logic.Graph import Graph
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
    try:
        graph.insert_node(info)
        return JSONResponse(content={"message": "Edge inserted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/insert_edge")
async def insert_edge(start: str, end: str, weight=1):
    try:
        graph.insert_edge(start, end, weight)
        return JSONResponse(content={"message": "Edge inserted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/update_node")
async def update_node(old_info: str, new_info: str):
    try:
        graph.update_node(old_info, new_info)
        return JSONResponse(content={"message": "Node updated successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/update_edge")
async def update_edge(start: str, end: str, weight=1):
    try:
        graph.update_edge(start, end, weight)
        return JSONResponse(content={"message": "Node updated successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/delete_node")
async def delete_node(info: str):
    try:
        graph.delete_node(info)
        return JSONResponse(content={"message": "Node deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/delete_edge")
async def delete_edge(start: str, end: str):
    try:
        graph.delete_edge(start, end)
        return JSONResponse(content={"message": "Edge deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
