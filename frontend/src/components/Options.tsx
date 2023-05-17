import { Button, Form, FormInstance, Input, Modal } from 'antd'
import React, { useRef, useState } from 'react'
import { clearGraph, insertNode } from '../services/apiServices';

interface OptionsProps {
  reloadGraph: ()=>void
}

const Options: React.FC<OptionsProps> = ({reloadGraph}) => {
  const [currentModal, setCurrentModal] = useState<string>();
  const insertForm = useRef<FormInstance<any>>(null);
  const handleInsert = () => {
    insertForm.current?.validateFields()
    .then(()=>{
      const info = insertForm.current?.getFieldValue('node_info');
      insertNode(info)
      .then(()=>{
        reloadGraph();
      })
      .catch(()=>{});
      setCurrentModal(undefined);
    })
    .catch(()=>{});
  }

  const handleEnter: React.KeyboardEventHandler<HTMLFormElement> = (e) => {
    if (e.key==='Enter') {
      switch (currentModal) {
        case 'insert_node':
            handleInsert()
          break;
      
        default:
          break;
      }
    }
  }

  const hanldeClearGraph = () => {
    clearGraph()
    .then(()=>reloadGraph())
    .catch(()=>{})
  }
  return (
    <div className='border-r-2 flex flex-col gap-4 px-8 my-8 pt-4'>
        <Button onClick={hanldeClearGraph}>New graph</Button>
        <Button onClick={()=>setCurrentModal('insert_node')}>Insert node</Button>
        <Button>Import graph</Button>
        <Button>Export Graph</Button>
        {currentModal==='insert_node' &&
          <Modal
            title='Insert node'
            centered
            open={true}
            onCancel={()=>setCurrentModal(undefined)}
            onOk={handleInsert}
          >
            <Form
              ref={insertForm}
              onKeyDown={handleEnter}
            >
              <Form.Item
                name='node_info'
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

export default Options