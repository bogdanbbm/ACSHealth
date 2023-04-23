import './App.css';
import React, {Component} from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import Home from './component/home/home';
import MedicalData from './component/medicalData/medicalData';
import Appointments from './component/appointments/appointments';
import Medics from './component/medics/Medics';
import NotFound from './component/notFound';

class App extends Component {
  render() {
    return (

      <Router>
        <div className="App">
          <nav>
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
              <li>
                <Link to="/medics">Medics</Link>
              </li>
            </ul>
          </nav>

          <Routes>
            <Route exact path="/" element={<Home />}></Route>
            <Route exact path="/medicalData" element={<MedicalData />}></Route>
            <Route exact path="/appointments" element={<Appointments />}></Route>
            <Route exact path="/medics" element={<Medics />}></Route>
            <Route path="*" element={<NotFound />}></Route>
          </Routes>
        </div>
      </Router>

    );
  }
}

export default App;
