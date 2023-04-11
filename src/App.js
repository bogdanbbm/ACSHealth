import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');

  const handleClick = async () => {
    const response = await axios.get('http://localhost:5001');
    console.log(response)
    setMessage(response.data);
  };
  return (


    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <button onClick={handleClick}>Get Message</button>
        <p>{message}</p>
      </header>
    </div>


  );
}

function Button() {
  const [message, setMessage] = useState('');

  const handleClick = async () => {
    const response = await axios.get('192.168.1.160:5000/');
    setMessage(response.data);
  };

  return (
    <div>
      <button onClick={handleClick}>Get Message</button>
      <p>{message}</p>
    </div>
  );
}

export default App;
export { Button };
