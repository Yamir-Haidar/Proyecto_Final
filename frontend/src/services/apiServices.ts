import axios, { Method } from "axios";

const API = 'http://localhost:8000';

const axiosRequest = async (method: Method, url: string, data: any = null) => {
  url = `${API}${url}`
    return axios({
        ...{method, data, url}
    })
}

export const getNodes = async () => {
  return axiosRequest('get', '/get_nodes');
};
