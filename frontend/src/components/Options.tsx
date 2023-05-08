import { Button } from 'antd'
import React from 'react'

const Options = () => {
  return (
    <div className='border-r-2 flex flex-col gap-4 px-8 my-8 pt-4'>
        <Button>New graph</Button>
        <Button>Insert node</Button>
        <Button>Import graph</Button>
        <Button>Export Graph</Button>
    </div>
  )
}

export default Options