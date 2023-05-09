import axios, { Method } from "axios";

const API = 'http://localhost:8000';

const axiosRequest = async (method: Method, url: string, params: any = null) => {
  url = `${API}${url}`
    return axios({
        ...{method, url, params}
    })
};

export const getNodes = async () => {
  return axiosRequest('get', '/get_nodes');
};

export const insertNode = async (info: string) => {
  return axiosRequest('post', '/insert_node', {...{info}});
};

export const insertEdge = async (start: string, end: string) => {
  return axiosRequest('post', '/insert_edge', {...{start, end}});
};
