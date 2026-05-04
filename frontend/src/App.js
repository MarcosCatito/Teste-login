import React, { useState } from 'react';


function App() {
  const [isLogin, setIsLogin] = useState(true);
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
      const endpoint = isLogin ? 'login' : 'register';
      const response = await fetch(`http://localhost:5000/${endpoint}`, {
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
        
        if (!isLogin) {
          // Store token and user info
          localStorage.setItem('token', data.token);
          localStorage.setItem('user', data.user);
          
          // Redirect to success page after 1 second
          setTimeout(() => {
            window.location.href = '/success';
          }, 1000);
        }
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

  const toggleForm = () => {
    setIsLogin(!isLogin);
    setMessage('');
    setFormData({ username: '', password: '' });
  };

  if (window.location.pathname === '/success') {
    return (
      <div className="container">
        <h1>Welcome!</h1>
        <div style={{ textAlign: 'center', padding: '2rem 0' }}>
          <h2 style={{ color: '#27ae60', marginBottom: '1rem' }}>
            Registration Successful! 
          </h2>
          <p style={{ color: '#666', marginBottom: '1rem' }}>
            Welcome, {localStorage.getItem('user')}!
          </p>
          <p style={{ color: '#666', fontSize: '0.9rem' }}>
            You have successfully registered and logged in.
          </p>
          <button 
            onClick={() => {
              localStorage.clear();
              window.location.href = '/';
            }}
            style={{ marginTop: '2rem', maxWidth: '200px' }}
          >
            Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>{isLogin ? 'Login' : 'Register'}</h1>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
            minLength={3}
            placeholder="Enter your username"
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
            required
            minLength={6}
            placeholder="Enter your password"
          />
        </div>
        
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Processing...' : (isLogin ? 'Login' : 'Register')}
        </button>
        
        {message && (
          <div className={isSuccess ? 'success' : 'error'}>
            {message}
          </div>
        )}
      </form>
      
      <div className="toggle-form">
        {isLogin ? "Don't have an account? " : "Already have an account? "}
        <a href="#" onClick={(e) => { e.preventDefault(); toggleForm(); }}>
          {isLogin ? 'Register' : 'Login'}
        </a>
      </div>
    </div>
  );
}

export default App;
