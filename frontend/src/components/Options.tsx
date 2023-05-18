import { Button, Form, FormInstance, Input, Modal, Select, Upload } from 'antd'
import React, { useRef, useState } from 'react'
import { breadthFirstSearch, clearGraph, depthFirstSearch, insertNode } from '../services/apiServices';
import { DefaultOptionType } from 'antd/es/select';
import { InboxOutlined, UploadOutlined } from '@ant-design/icons';

interface OptionsProps {
  reloadGraph: ()=>void
}

const Options: React.FC<OptionsProps> = ({reloadGraph}) => {
  const [currentModal, setCurrentModal] = useState<string>();
  const insertForm = useRef<FormInstance<any>>(null);
  const travelsForm = useRef<FormInstance<any>>(null);

  const options: DefaultOptionType[] = [
    {
      label: 'Breadth First',
      value: 'breadthFirst',
    },
    {
      label: 'Depth First',
      value: 'depthFirst',
    },
  ]

  const normFile = (e: any) => {
    console.log('Upload event:', e);
    if (Array.isArray(e)) {
      return e;
    }
    return e?.fileList;
  };

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

  const handleTravel = () => {
    travelsForm.current?.validateFields()
    .then(()=>{
      const info = travelsForm.current?.getFieldValue('node_info_travels');
      const travel = travelsForm.current?.getFieldValue('travel');
      switch (travel) {
        case 'breadthFirst':
          breadthFirstSearch(info)
          .then((data)=>console.log(data.data))
          .catch(()=>{});
          break;
          case 'depthFirst':
            depthFirstSearch(info)
            .then((data)=>console.log(data.data))
            .catch(()=>{});
          break;
        default:
          break;
      }
      setCurrentModal(undefined);
    })
    .catch(()=>{});
  }

  const handleUpload = () => {

  }

  const handleEnter: React.KeyboardEventHandler<HTMLFormElement> = (e) => {
    if (e.key==='Enter') {
      switch (currentModal) {
        case 'insert_node':
          handleInsert();
          break;
        case 'travels':
          handleTravel();
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
        <Button onClick={()=>setCurrentModal('travels')}>Travels</Button>
        <Button onClick={()=>setCurrentModal('load')}>Import graph</Button>
        <Button onClick={()=>setCurrentModal('')}>Export Graph</Button>
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
        {currentModal==='travels' &&
          <Modal
            title='Travels'
            centered
            open={true}
            onCancel={()=>setCurrentModal(undefined)}
            onOk={handleTravel}
          >
            <Form
              ref={travelsForm}
              onKeyDown={handleEnter}
            >
              <Form.Item
                name='node_info_travels'
                label='Info'
                rules={[
                  {required: true, message: 'Input the info!'}
                ]}
              >
                <Input/>
              </Form.Item>
              <Form.Item
                name='travel'
                label='Travel'
                rules={[
                  {required: true, message: 'Select the travel!'}
                ]}
              >
                <Select {...{options}}/>
              </Form.Item>
            </Form>
          </Modal>
        }
        {currentModal==='load' &&
          <Modal
            title='Load graph'
            centered
            open={true}
            onCancel={()=>setCurrentModal(undefined)}
            onOk={handleUpload}
          >
            <Form
              ref={travelsForm}
              onKeyDown={handleEnter}
            >
              <Form.Item name="dragger" valuePropName="fileList" getValueFromEvent={normFile} noStyle>
                <Upload.Dragger name="files" action="/upload.do">
                  <p className="ant-upload-drag-icon">
                    <InboxOutlined />
                  </p>
                  <p className="ant-upload-text">Click or drag file to this area to upload</p>
                  <p className="ant-upload-hint">Support for a single or bulk upload.</p>
                </Upload.Dragger>
              </Form.Item>
            </Form>
          </Modal>
        }



        
    </div>
  )
}

export default Options