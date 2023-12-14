import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import './RegistrationComponent.css';
import { Link, useNavigate } from 'react-router-dom';
const RegistrationComponent = ({ onRegister, onCancel }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate(); 
  const handleRegister = () => {
    const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const isPasswordValid = password.length >= 6;
    const isPasswordMatch = password === confirmPassword;
    if (isEmailValid && isPasswordValid && isPasswordMatch) {
      onRegister({  email, password });
      navigate('/home');
    } else {
      if (!isEmailValid) {
        alert('Invalid email format');
      }
      if (!isPasswordValid) {
        alert('Password should be at least 6 characters long');
      }
      if (!isPasswordMatch) {
        alert('Password and Confirm Password do not match');
      }
      alert('Invalid registration data');
    }
  };
  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    }
  };
  const containerStyle = {
    maxWidth: '400px',
    margin: 'auto',
    padding: '10px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    backgroundImage: 'url("https://i.pinimg.com/originals/ff/82/83/ff828330992531e3332ba85153e33562.jpg")',
    backgroundSize: 'cover', 
  };
  const logoStyle = {
    width: '150px',
    height: '150px',
    paddingLeft: '115px',  
  };
  return (
    <div style={containerStyle}>
       <img src="https://www.skcet.ac.in/script/ICTAL/images/SKCET%20Logo.JPG" alt="Logo" style={logoStyle} />
      <div style={{ maxWidth: '100%', padding: '10px', borderRadius: '10px' }}>
        <h1 style={{ fontSize: '1.5rem', color: 'black', fontFamily: 'cursive' }}>REGISTRATION FORM</h1>
        <TextField
          label="Email"
          variant="outlined"
          fullWidth
          margin="normal"
          style={{ width: '80%', marginBottom: '15px' ,}}
          value={email}
          onChange={(e) => setEmail(e.target.value)}/>
        <TextField
          label="Password"
          variant="outlined"
          fullWidth
          margin="normal"
          style={{ width: '80%', marginBottom: '15px' ,}}
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}/>
        <TextField
          label="Confirm Password"
          variant="outlined"
          fullWidth
          margin="normal"
          style={{ width: '80%', marginBottom: '15px' ,}}
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}/>
        <Button variant="contained" color="primary" onClick={handleRegister}>
          Submit
        </Button>
        <Button variant="outlined" color="secondary" onClick={handleCancel}>
          Cancel
        </Button><br></br>
      </div>
    </div>
  );
};
export default RegistrationComponent;
