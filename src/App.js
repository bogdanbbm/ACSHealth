import './App.css';
import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import Home from './component/home/Home';
import MedicalData from './component/medicalData/MedicalData';
import Appointments from './component/appointments/Appointments';
import Medics from './component/medics/Medics';
import NotFound from './component/NotFound';
import Register from './component/login/Register';
import Login from './component/login/Login';
import LoginAccButton from './component/login_acc_button/LoginAccButton';
import useToken from './hooks/useToken';
import PropTypes from 'prop-types';

class AppComponent extends Component {
  render() {
    return (

      <Router>
        <div className="navbar">
          <nav>
            <ul>
              <li>
                <Link to="/">Home</Link>
              </li>
              <li>
                <Link to="/medicalData">Data</Link>
              </li>
              <li>
                <Link to="/appointments">Appointments</Link>
              </li>
              <li>
                <Link to="/medics">Medics</Link>
              </li>
              <div className="spacer"></div>
            </ul>

            <div className="login-acc-button">
              <LoginAccButton />
            </div>


          </nav>

          <Routes>
            <Route exact path="/" element={<Home />}></Route>
            <Route exact path="/medicalData" element={<MedicalData />}></Route>
            <Route exact path="/appointments" element={<Appointments />}></Route>
            <Route exact path="/medics" element={<Medics />}></Route>
            <Route exact path="/login" element={<Login  setToken={this.props.setToken}/>}></Route>
            <Route exact path="/register" element={<Register />}></Route>
            <Route path="*" element={<NotFound />}></Route>
          </Routes>
        </div>
      </Router>

    );
  }
}

AppComponent.propTypes = {
  setToken: PropTypes.func.isRequired
};

function App() {
  const {setToken} = useToken();

  return (
    <AppComponent setToken={setToken}/>
  );
}

export default App;
