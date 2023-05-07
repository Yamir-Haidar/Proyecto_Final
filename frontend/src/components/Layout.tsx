import React from 'react'
import Header from './Header'
import MainGraph from './Graph'
import Options from './Options'

const Layout: React.FC = () => {
  return (
    <div className='flex flex-col h-screen'>
        <Header/>
        <div className='flex flex-row flex-1'>
            <Options/>
            <MainGraph/>
        </div>
        
    </div>
  )
}

export default Layout