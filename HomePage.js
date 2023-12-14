import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const SmartBoard = () => {
  const [dateTime, setDateTime] = useState(new Date());
  const [welcomeMessage, setWelcomeMessage] = useState('The board you"ll never get bored of ;)');
  const navigate = useNavigate(); // Initialize the useNavigate hook

  useEffect(() => {
    const interval = setInterval(() => {
      setDateTime(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const divStyle = {
    backgroundSize: 'cover',
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    color: 'white',
  };

  return (
    <div style={divStyle}>
      <div>
        <p>Date: {dateTime.toLocaleDateString()}</p>
        <p>Time: {dateTime.toLocaleTimeString()}</p>
      </div>
      <h1>{welcomeMessage}</h1>
      {/* Navigate directly to the login page */}
      <button onClick={() => navigate('/login')}>Go to Login</button>
    </div>
  );
};

export default SmartBoard;
