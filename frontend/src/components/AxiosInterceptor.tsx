import { notification } from 'antd';
import axios from 'axios';
import React, { useEffect } from 'react'

const AxiosInterceptor: React.FC<{children: React.ReactNode}> = ({children}) => {
    useEffect(() => {
        const interceptor = axios.interceptors.response.use(
            response => {
            console.log('Respuesta exitosa:', response);
            const {message} = response.data
            if (message) {
                notification.success({...{message}});
            }
            return response;
            },
            error => {
            console.log('Error de respuesta:', error);
            if (!error.response) {
                error.response = {};
                error.response.data = {};
                error.response.data.detail = error.message;
                error.response.status = 0;
            };
            notification.error({message: error.response.data.detail});
            return Promise.reject(error);
            }
        );

        return () => {
            axios.interceptors.response.eject(interceptor);
        };
    }, []);
    
  return (
    <>
        {children}
    </>
  )
}

export default AxiosInterceptor