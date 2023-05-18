import React, { useRef, useState, useEffect } from 'react'
import Graph, { Options, graphData, graphEvents } from "react-graph-vis";
import FloatOptions, { FloatOptionsProps } from './FloatOptions';
import { Form, FormInstance, Input, Modal } from 'antd'
import { IdType } from 'vis';
import {  deleteEdge, deleteNode, insertEdge, updateNode } from '../services/apiServices';

interface MainGraphProps {
  graph: graphData;
  reloadGraph: ()=>void;
}

const MainGraph: React.FC<MainGraphProps> = ({graph, reloadGraph}) => {
  const formUpdateNode = useRef<FormInstance<any>>(null);
  const [currentModal, setCurrentModal] = useState<string>();
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

  const hideModal = () => {
    setCurrentModal('');
  }

  const handleEnter: React.KeyboardEventHandler<HTMLFormElement> = (e) => {
    if (e.key==='Enter') {
      switch (currentModal) {
        case 'update_node':
          handleUpdateNode()
          break;
      
        default:
          break;
      }
    }
  }

  //nodes
  const handleUpdateNode = () => {
    formUpdateNode.current?.validateFields()
    .then(()=>{
      const info = formUpdateNode.current?.getFieldValue('node_info_update');
      const oldInfo = graphRef.current?.Network.getSelectedNodes()[0];
      updateNode(String(oldInfo), info)
      .then((data)=>{hideModal(); reloadGraph()})
      .catch(()=>{});
    })
    .catch(()=>{})
  }
  const removeNode = (node: IdType) => {
    deleteNode(String(node))
    .then(()=>{
      graphRef.current?.Network.deleteSelected();
    })
    .catch(()=>{})
  }
  
  //Edges
  const preLinkNode = (node: IdType) => {
    setLinking(node);
    if (graphRef.current) {
      graphRef.current.container.current.setAttribute('style', 'cursor: pointer');
    }
  }
  const removeEdge = (edge: IdType) => {
    const nodes = graphRef.current?.Network.getConnectedNodes(edge);
    if (nodes && nodes.length===2) {
      deleteEdge(String(nodes[0]), String(nodes[1]))
      .then(()=>{
        graphRef.current?.Network.deleteSelected();
      })
      .catch(()=>{});
    }
    
  }
  
  useEffect(() => {
    //console.log(graph)
  }, [graph])

  const events: graphEvents = {
    oncontext: function(event: any) {
      event.event.preventDefault()
      const {x, y} = event.pointer.DOM;
      if (graphRef.current) {
        const node = graphRef.current.Network.getNodeAt({x: x, y: y});
        if (node) {
          graphRef.current.Network.selectNodes([node]);
          setFloatOptions({visible:true, x: x, y: y, options: [
            {label: 'Update', click: ()=>setCurrentModal('update_node')},
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
        {currentModal === 'update_node' &&
          <Modal
          title='Update node'
              centered
              open={true}
              onCancel={()=>hideModal()}
              onOk={handleUpdateNode}
            >
              <Form
                ref={formUpdateNode}
                onKeyDown={handleEnter}
              >
                <Form.Item
                  name='node_info_update'
                  label='Info'
                  rules={[
                    {required: true, message: 'Select the info!'}
                  ]}
                >
                  <Input/>
                </Form.Item>
              </Form>
          </Modal>
        }
        
    </div>
  )
}

export default MainGraph