import os
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from backend.Graph import Graph
from backend.utils import generate_text

DIRECTORY = "saved_graphs/"
EXTENSION_FILE = ".yaor"

graph = Graph()
graph.insert_node("1")
graph.insert_node("2")
graph.insert_node("3")
graph.insert_node("4")
graph.insert_node("5")
graph.insert_node("6")
graph.insert_node("7")
graph.insert_node("8")
graph.insert_edge("1", "2")
graph.insert_edge("1", "3")
graph.insert_edge("1", "4")
graph.insert_edge("2", "5")
graph.insert_edge("3", "6")
graph.insert_edge("3", "7")
graph.insert_edge("4", "7")
graph.insert_edge("4", "8")

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
async def insert_edge(start: str, end: str, weight="1"):
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
        return JSONResponse(content={"message": "Edge deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/bft")
async def breadth_first_traversal(start: str):
    try:
        result = graph.breadth_first_traversal(start)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/dft")
async def depth_first_traversal(start: str):
    try:
        result = graph.depth_first_traversal(start)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/save")
async def save():
    try:
        file_dir = DIRECTORY + generate_text() + EXTENSION_FILE
        if len(graph.nodes) == 0:
            raise Exception("Nothing to save")
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
        graph.save(str(file_dir))
        return FileResponse(path=file_dir)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/load")
async def load(file: UploadFile):
    try:
        if not file.filename.endswith(EXTENSION_FILE):
            raise Exception("Invalid file")
        content = await file.read()
        file_str = content.decode("utf-8").replace("\r\n", '\n')
        graph.load(file_str)
        return JSONResponse(content=graph.get_nodes_and_edges())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
