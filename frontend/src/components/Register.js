import React, { useState } from 'react';
import './styles.css';

function Register({ onToggleForm, onRegisterSuccess }) {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [message, setMessage] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
        setIsSuccess(true);
        
        // Store token and user info
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', data.user);
        
        // Notify parent component
        if (onRegisterSuccess) {
          onRegisterSuccess(data);
        }
        
        // Redirect to success page after 1 second
        setTimeout(() => {
          window.location.href = '/success';
        }, 1000);
      } else {
        setMessage(data.error || 'An error occurred');
        setIsSuccess(false);
      }
    } catch (error) {
      setMessage('Connection error. Please try again.');
      setIsSuccess(false);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Enter your username"
            required
            minLength="3"
            maxLength="50"
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            required
            minLength="6"
          />
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Registering...' : 'Register'}
        </button>
      </form>
      
      {message && (
        <div className={`message ${isSuccess ? 'success' : 'error'}`}>
          {message}
        </div>
      )}
      
      <div className="toggle-form">
        Already have an account? 
        <a href="#" onClick={(e) => {
          e.preventDefault();
          if (onToggleForm) onToggleForm();
        }}>
          Login
        </a>
      </div>
    </div>
  );
}

export default Register;
