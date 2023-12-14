import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginComponent from './components login/LoginComponent';
import RegistrationComponent from './components reg/RegistrationComponent';
import './App.css';
import SmartBoard from './components extra/HomePage';
import Home from './components extra/homeage';
const App = () => {
  const handleLogin = (credentials) => {
    alert('Login Successful', credentials);
  };
  const handleCancel = () => {
    alert('Login canceled');
  };
  const handleRegister = (credentials) => {
    alert('Registration Successful', credentials);
  };
  return (
          <Router>
            <Routes>
              <Route path="/" element={<SmartBoard/>} />
              <Route path="/login" element={<LoginComponent onLogin={handleLogin} onCancel={handleCancel} />} />
              <Route
                path="/register"
                element={<RegistrationComponent onRegister={handleRegister} onCancel={handleCancel} />}
              />
              <Route
                path="/home"
                element={ <Home/>}
              />

            </Routes>
          </Router>
  );
};
export default App;
