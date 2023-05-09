import React, { useState, useEffect } from 'react'
import Header from './Header'
import MainGraph from './Graph'
import Options from './Options'
import { graphData } from 'react-graph-vis'
import { graphDataAdapter } from '../services/adapters'
import { getNodes } from '../services/apiServices'

const Layout: React.FC = () => {
  const [graph, setGraph] = useState<graphData>({
    nodes: [],
    edges: [
      { from: 1, to: 2, shadow: true },
      { from: 1, to: 3 },
      { from: 2, to: 4 },
      { from: 2, to: 5 },
      { from: 5, to: 2 },
    ]
  })
  const reloadGraph = () => {
    getNodes()
    .then((data)=>setGraph(graphDataAdapter(data.data)))
    .catch((error)=>console.log(error))
  }

  useEffect(() => {
    reloadGraph();
  }, [])
  
  return (
    <div className='flex flex-col h-screen'>
        <Header/>
        <div className='flex flex-row flex-1'>
            <Options {...{reloadGraph}}/>
            <MainGraph {...{graph, reloadGraph}}/>
        </div>
        
    </div>
  )
}

export default Layout