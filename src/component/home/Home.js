import logo from '../../acs-health-logo.svg';
import './Home.css';
import React from 'react';

function Home() {
  return (
    <div className="Home">
      <header className="Home-header">
        <img src={logo} className="App-logo" alt="logo" />

        <h1 className="Home-text">
          Welcome to ACSHealth!
        </h1>
      </header>
    </div>
  );
}

export default Home;
