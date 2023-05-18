from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from logic.Graph import Graph

graph = Graph()
graph.insert_node("A")
graph.insert_node("B")
graph.insert_node("C")
graph.insert_node("D")
graph.insert_edge("A", "B")
graph.insert_edge("C", "B")
graph.insert_edge("D", "B")


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


@app.delete("/clear_graph")
async def clear_graph():
    graph.clear_graph()
    return JSONResponse(content={"message": "Cleared graph"}, status_code=200)


@app.post("/insert_node")
async def insert_node(info: str):
    try:
        graph.insert_node(info)
        return JSONResponse(content={"message": "Node inserted successfully"}, status_code=200)
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
        return JSONResponse(content={"message": "Edge updated successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/delete_node")
async def delete_node(info: str):
    try:
        graph.delete_node(info)
        return JSONResponse(content={"message": "Node deleted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/delete_edge")
async def delete_edge(start: str, end: str):
    try:
        graph.delete_edge(start, end)
        return JSONResponse(content={"message": "Edge deleted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/bfs")
async def breadth_first_search(start: str):
    try:
        result = graph.breadth_first_search(start)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/dfs")
async def depth_first_search(start: str):
    try:
        result = graph.depth_first_search(start)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/save")
async def save(filename: str):
    return graph.save(filename)


@app.post("/load")
async def load(file: UploadFile):
    try:
        content = await file.read()
        file_str = content.decode("utf-8").replace("\r\n", '\n')
        graph = Graph.load(file_str)
        return JSONResponse(status_code=200, content=graph)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/load_ok")
async def load_ok():
    return JSONResponse(status_code=200, content=graph.get_nodes_and_edges())


@app.post("/export")
async def export_graph(filename: str):
    return graph.export_graph(filename)


@app.get("/import")
async def import_graph(filename: str):
    return graph.import_graph(filename)
