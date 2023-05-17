import React from 'react';
import './App.css';
import Layout from './components/Layout';
import AxiosInterceptor from './components/AxiosInterceptor';

const App: React.FC = () => {
  return (
    <div className="App">
      <AxiosInterceptor>
        <Layout/>
      </AxiosInterceptor>
    </div>
  );
}

export default App;
