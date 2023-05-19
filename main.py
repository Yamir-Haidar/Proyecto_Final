import os
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from logic.Graph import Graph
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
        return JSONResponse(content={"message": "Edge deleted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/bft")
async def breadth_first_traversal(start: str):
    try:
        result = graph.breadth_first_traversal(start)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/dft")
async def depth_first_traversal(start: str):
    try:
        result = graph.depth_first_traversal(start)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/save")
async def save(path: str, name: str):
    if not path or not name:
        raise HTTPException(status_code=400, detail="Some data is missing")
    # Comprobar si la ruta existe
    if not os.path.exists(path):
        raise HTTPException(status_code=400, detail="Path doesn't exists")
    # Comprobar si la ruta es un directorio
    if not os.path.isdir(path):
        raise HTTPException(status_code=400, detail="Path is not a directory")
    # Comprobar si el archivo ya existe
    archivo_completo = os.path.join(path, name + EXTENSION_FILE)
    if os.path.exists(archivo_completo):
        raise HTTPException(status_code=400, detail="Already existing file")
    # Crear el archivo
    graph.save(archivo_completo)
    # Devolver la respuesta
    return JSONResponse(status_code=200, content="File successfully saved")


@app.post("/load")
async def load(file: UploadFile):
    try:
        if not file.filename.endswith(EXTENSION_FILE):
            raise Exception("Invalid file")
        content = await file.read()
        file_str = content.decode("utf-8").replace("\r\n", '\n')
        graph.load(file_str)
        return JSONResponse(status_code=200, content=graph.get_nodes_and_edges())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/export")
async def export_graph(filename: str):
    return graph.export_graph(filename)


@app.get("/import")
async def import_graph(filename: str):
    return graph.import_graph(filename)
