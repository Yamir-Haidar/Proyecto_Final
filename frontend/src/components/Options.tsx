import styled from '@emotion/styled';
import { Button, Form, FormInstance, Input, Modal } from 'antd'
import React, { useRef, useState } from 'react'

const ModalStyled = styled(Modal)`
  .ant-btn-primary {
    background-color: #1677ff ;
  }
`

const Options = () => {
  const [currentModal, setCurrentModal] = useState<string>();
  const insertForm = useRef<FormInstance<any>>(null);
  const handleInsert = () => {
    insertForm.current?.validateFields()
    .then(()=>{
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