import './App.css';
import React, {Component} from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import Home from "./component/home";
import MedicalData from "./component/medicalData";
import Appointments from "./component/appointments";

class App extends Component {
  render() {
    return (

      <Router>
        <div className="App">
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/medicalData">Medical Data</Link>
            </li>
            <li>
              <Link to="/appointments">Appointments</Link>
            </li>
          </ul>
          <Routes>
            <Route exact path='/' element={<Home />}></Route>
            <Route exact path='/medicalData' element={<MedicalData />}></Route>
            <Route exact path='/appointments' element={<Appointments />}></Route>
          </Routes>
        </div>
      </Router>

    );
  }
}

export default App;

