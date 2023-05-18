import { Button, Form, FormInstance, Input, Modal, Select, Upload, UploadFile, UploadProps, notification } from 'antd'
import React, { useRef, useState } from 'react'
import { breadthFirstSearch, clearGraph, depthFirstSearch, insertNode, load } from '../services/apiServices';
import { DefaultOptionType } from 'antd/es/select';
import { InboxOutlined, LoadingOutlined } from '@ant-design/icons';
import { RcFile } from 'antd/es/upload';

interface OptionsProps {
  reloadGraph: ()=>void
}

const Options: React.FC<OptionsProps> = ({reloadGraph}) => {
  const [uploading, setUploading] = useState(false);
  const [currentModal, setCurrentModal] = useState<string>();
  const insertForm = useRef<FormInstance<any>>(null);
  const uploadForm = useRef<FormInstance<any>>(null);
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

  const props: UploadProps = {
    name: 'file',
    multiple: false,
    maxCount: 1,
    // action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76',
    onChange(info) {
      const { status } = info.file;
      if (status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (status === 'done') {
        console.log(`${info.file.name} file uploaded successfully.`);
      } else if (status === 'error') {
        console.log(`${info.file.name} file upload failed.`);
      }
    },

    
    
    beforeUpload(file) {
      const formData = new FormData();
      
      formData.append('file', file as RcFile);
      setUploading(true);
      load(formData)
      .then(()=>{setUploading(false)})
      .catch(()=>{setUploading(false)})
      return false;
    },
    onDrop(e) {
      console.log('Dropped files', e.dataTransfer.files);
    },
  }

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
    uploadForm.current?.validateFields()
    .then()
    .catch();
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
              ref={uploadForm}
              onKeyDown={handleEnter}
            >
              <Form.Item
                name="dragger"
                valuePropName='fileList'
                getValueFromEvent={normFile}
                noStyle
                rules={[
                  {required: true, message: 'Pleade upload!'}
                ]}
              >
                <Upload.Dragger {...props}>
                  <p className="ant-upload-drag-icon">
                    {!uploading &&
                      <InboxOutlined />
                    }
                    {uploading &&
                      <LoadingOutlined />
                    }
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