import axios, { Method } from "axios";

export const API = 'http://localhost:8000';

const axiosRequest = async (method: Method, url: string, params: any = null, type: 'file' | null = null) => {
  url = `${API}${url}`
    if (type) {
      return axios({
        ...{method, url, data: params, headers: {"Content-Type": "multipart/form-data"}}
      })
    } else {
      return axios({
        ...{method, url, params}
      })
    }
};


//Nodes
export const getNodes = async () => {
  return axiosRequest('get', '/get_nodes');
};
export const insertNode = async (info: string) => {
  return axiosRequest('post', '/insert_node', {...{info}});
};
export const updateNode = async (old_info: string, new_info: string) => {
  return axiosRequest('post', '/update_node', {...{old_info, new_info}});
};
export const deleteNode = async (info: string) => {
  return axiosRequest('delete', '/delete_node', {...{info}});
};
export const clearGraph = async () => {
  return axiosRequest('delete', '/clear_graph');
};

//Edges
export const insertEdge = async (start: string, end: string) => {
  return axiosRequest('post', '/insert_edge', {...{start, end}});
};
export const updateEdge = async (start: string, end: string, weight: string) => {
  return axiosRequest('post', '/update_edge', {...{start, end, weight}});
};
export const deleteEdge = async (start: string, end: string) => {
  return axiosRequest('delete', '/delete_edge', {...{start, end}});
};

//Searchs
export const breadthFirstSearch = async (start: string) => {
  return axiosRequest('get', '/bfs', {...{start}});
};
export const depthFirstSearch = async (start: string) => {
  return axiosRequest('get', '/dfs', {...{start}});
};

//File
export const save = async (filename: string) => {
  return axiosRequest('get', '/save', {...{filename}});
};
export const load = async (file: FormData) => {
  return axiosRequest('post', '/load', file, 'file');
};