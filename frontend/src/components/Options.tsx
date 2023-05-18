import { Button, Form, FormInstance, Modal, Popconfirm, Upload, UploadProps } from 'antd'
import React, { useRef, useState } from 'react'
import { clearGraph, load, save } from '../services/apiServices';
import { InboxOutlined, LoadingOutlined, QuestionCircleOutlined } from '@ant-design/icons';
import { RcFile } from 'antd/es/upload';

interface OptionsProps {
  reloadGraph: ()=>void
}

const Options: React.FC<OptionsProps> = ({reloadGraph}) => {
  const [uploading, setUploading] = useState(false);
  const [currentModal, setCurrentModal] = useState<string>();
  const uploadForm = useRef<FormInstance<any>>(null);

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

  const handleUpload = () => {
    uploadForm.current?.validateFields()
    .then()
    .catch();
  }

  const handleEnter: React.KeyboardEventHandler<HTMLFormElement> = (e) => {
    if (e.key==='Enter') {
      switch (currentModal) {
        
        default:
          break;
      }
    }
  }

  const handleExport = () => {
    save("asd")
    .then()
    .catch();
  }

  const hanldeClearGraph = () => {
    clearGraph()
    .then(()=>reloadGraph())
    .catch(()=>{})
  }
  return (
    <div className='border-r-2 flex flex-col gap-4 px-8 my-8 pt-4'>
        <Popconfirm
          title="New graph"
          description="Are you sure to delete this graph?"
          placement='rightTop'
          onConfirm={hanldeClearGraph}
        >
          <Button>New graph</Button>
        </Popconfirm>
        <Button onClick={()=>setCurrentModal('load')}>Import graph</Button>
        <Button onClick={handleExport}>Export Graph</Button>
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