import { graphData } from "react-graph-vis";
import { GraphData } from "./interfaces"
import { Edge, Node } from "vis";

export const graphDataAdapter = ({nodes, edges}: GraphData): graphData => {
    console.log(edges)
    const nodesData: Node[] = [];
    const edgesData: Edge[] = [];
    console.log(nodes)
    nodes.forEach((node)=>nodesData.push({ id: node, label: node, shadow: true, shape: 'circle' },));
    edges.forEach((edge)=>edgesData.push({ from: edge[0], to: edge[1], shadow: true, label: edge[2] },));
    const data: graphData = {nodes: nodesData, edges: edgesData};
    return data;
}