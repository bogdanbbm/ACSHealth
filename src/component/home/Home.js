import logo from '../../logo.svg';
import '../../App.css';
import React, { useState } from 'react';
import axios from 'axios';

function Home() {
  const [message, setMessage] = useState('');

  const apiURL = process.env.REACT_APP_API_URL;

  const handleClick = async () => {
    const response = await axios.get(apiURL);
    console.log(response);
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

export default Home;
