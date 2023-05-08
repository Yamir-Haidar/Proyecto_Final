import React, { useRef, useState } from 'react'
import Graph, { Network, Options, graphData, graphEvents } from "react-graph-vis";
import FloatOptions, { FloatOptionsProps } from './FloatOptions';

const MainGraph = () => {
  const [floatOptions, setFloatOptions] = useState<FloatOptionsProps>(
    {x: 0, y: 0, visible: false, options:[]}
  );
  const graphRef = useRef<Graph>(null);
  const [graph, setGraph] = useState<graphData>({
      nodes: [
        { id: 1, label: "Node 1", title: "node 1 tootip text" },
        { id: 2, label: "Node 2", title: "node 2 tootip text" },
        { id: 3, label: "Node 3", title: "node 3 tootip text" },
        { id: 4, label: "Node 4", title: "node 4 tootip text" },
        { id: 5, label: "Node 5", title: "node 5 tootip text" }
      ],
      edges: [
        { from: 1, to: 2 },
        { from: 1, to: 3 },
        { from: 2, to: 4 },
        { from: 2, to: 5 },
        { from: 5, to: 2 },
      ]
    }
  )
  const options: Options = {
      layout: {
        hierarchical: false, 
      },
      edges: {
        color: "#000000"
      },
      height: "100%"
    };

  const removeNode = (node: number) => {
    console.log(node);
    graphRef.current?.Network.deleteSelected();
  }

  const events: graphEvents = {
    oncontext: function(event: any) {
      event.event.preventDefault()
      const {x, y} = event.pointer.DOM;
      console.log(event)
      if (graphRef.current) {
        const node = graphRef.current.Network.getNodeAt({x: x, y: y});
        if (node) {
          graphRef.current.Network.selectNodes([node]);
          setFloatOptions({visible:true, x: x, y: y, options: [{label: 'Delete', click: ()=>removeNode(Number(node))}]})
        }
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
            console.log(network)
            console.log(network.getNodeAt)
          }}
        />
        <FloatOptions {...floatOptions} onCancel={()=>setFloatOptions({visible: false, x: 0, y: 0, options: []})}/>
    </div>
  )
}

export default MainGraph