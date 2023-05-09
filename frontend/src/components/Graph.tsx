import React, { useRef, useState, useEffect } from 'react'
import Graph, { Options, graphData, graphEvents } from "react-graph-vis";
import FloatOptions, { FloatOptionsProps } from './FloatOptions';
import { notification } from 'antd'
import { IdType } from 'vis';
import { insertEdge } from '../services/apiServices';

interface MainGraphProps {
  graph: graphData;
  reloadGraph: ()=>void;
}

const MainGraph: React.FC<MainGraphProps> = ({graph, reloadGraph}) => {
  const [floatOptions, setFloatOptions] = useState<FloatOptionsProps>(
    {x: 0, y: 0, visible: false, options:[]}
  );
  const graphRef = useRef<Graph>(null);
  const [linking, setLinking] = useState<IdType | null>(null);
  
  const options: Options = {
      layout: {
        hierarchical: false, 
      },
      edges: {
        color: "#000000"
      },
      height: "100%"
    };

  const removeNode = (node: IdType) => {
    graphRef.current?.Network.deleteSelected();
    notification.success({message: 'Successfully node deleted'});
  }

  
  
  useEffect(() => {
    console.log(graph)
  }, [graph])

  const preLinkNode = (node: IdType) => {
    setLinking(node);
    if (graphRef.current) {
      graphRef.current.container.current.setAttribute('style', 'cursor: pointer');
    }
  }

  const removeEdge = (edge: IdType) => {
    graphRef.current?.Network.deleteSelected();
    notification.success({message: 'Successfully edge deleted'});
  }

  const events: graphEvents = {
    oncontext: function(event: any) {
      event.event.preventDefault()
      const {x, y} = event.pointer.DOM;
      if (graphRef.current) {
        const node = graphRef.current.Network.getNodeAt({x: x, y: y});
        if (node) {
          graphRef.current.Network.selectNodes([node]);
          setFloatOptions({visible:true, x: x, y: y, options: [
            {label: 'Link', click: ()=>preLinkNode(node)},
            {label: 'Delete', click: ()=>removeNode(node)},
          ]})
        } else {
          const edge = graphRef.current.Network.getEdgeAt({x: x, y: y});
          if (edge) {
            graphRef.current.Network.selectEdges([edge]);
            setFloatOptions({visible:true, x: x, y: y, options: [{label: 'Delete', click: ()=>removeEdge(edge)}]})
          }
        }
      }
    },
    select: (event: any) => {
      if (linking) {
        if (event.nodes[0]) {
          insertEdge(String(linking), event.nodes[0]);
          reloadGraph();
        }
        setLinking(null);
        graphRef.current?.container.current.setAttribute('style', 'cursor: arrow');
      }
    }
  };
  return (
    <div className='flex flex-1 h-full'>
      <Graph
          ref={graphRef}
          graph={graph}
          options={options}
          events={events}
          getNetwork={network => {
            //  if you want access to vis.js network api you can set the state in a parent component using this property
          }}
        />
        <FloatOptions {...floatOptions} onCancel={()=>setFloatOptions({visible: false, x: 0, y: 0, options: []})}/>
    </div>
  )
}

export default MainGraph