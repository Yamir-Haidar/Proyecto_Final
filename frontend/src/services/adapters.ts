import { graphData } from "react-graph-vis";
import { GraphData } from "./interfaces"
import { Edge, Node } from "vis";
import { color } from "../settings";
import { darken, lighten } from "../utils/colors";

export const graphDataAdapter = ({nodes, edges}: GraphData): graphData => {
    const nodesData: Node[] = [];
    const edgesData: Edge[] = [];
    nodes.forEach((node)=>nodesData.push({
        id: node, 
        label: node, 
        shadow: true, 
        shape: 'circle', 
        color: {
            background: color.node, 
            border: darken(color.node, 20),
            highlight: {
                background: lighten(color.node, 20),
                border: color.node
            }
        } 
    },));
    edges.forEach((edge)=>edgesData.push({ from: edge[0], to: edge[1], shadow: true, label: String(edge[2]) },));
    const data: graphData = {nodes: nodesData, edges: edgesData};
    return data;
}