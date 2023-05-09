import styled from '@emotion/styled';
import { Button, Form, FormInstance, Input, Modal, notification } from 'antd'
import React, { useRef, useState } from 'react'
import { insertNode } from '../services/apiServices';

interface OptionsProps {
  reloadGraph: ()=>void
}

const ModalStyled = styled(Modal)`
  .ant-btn-primary {
    background-color: #1677ff ;
  }
`

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
        notification.success({message: 'Successfully node inserted'});
      })
      .catch((error)=>notification.error({message: error.response.data.detail}));
      setCurrentModal(undefined);
    })
    .catch(()=>{});
  }
  return (
    <div className='border-r-2 flex flex-col gap-4 px-8 my-8 pt-4'>
        <Button>New graph</Button>
        <Button onClick={()=>setCurrentModal('insert_node')}>Insert node</Button>
        <Button>Import graph</Button>
        <Button>Export Graph</Button>
        {currentModal==='insert_node' &&
          <ModalStyled
            title='Insert node'
            centered
            open={true}
            onCancel={()=>setCurrentModal(undefined)}
            onOk={handleInsert}
          >
            <Form
              ref={insertForm}
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
          </ModalStyled>
        }
        
    </div>
  )
}

export default Options