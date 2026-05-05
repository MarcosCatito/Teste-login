import React, { useState, useEffect } from 'react';
import './styles.css';

function SuccessPage() {
  const [user, setUser] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Get user info from localStorage
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(storedUser);
    }
    setIsLoading(false);
  }, []);

  const handleLogout = () => {
    // Clear all localStorage data
    localStorage.clear();
    // Redirect to login page
    window.location.href = '/';
  };

  if (isLoading) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Welcome!</h1>
      <div style={{ textAlign: 'center', padding: '2rem 0' }}>
        <h2 style={{ color: '#27ae60', marginBottom: '1rem' }}>
          Registration Successful! 
        </h2>
        <p style={{ color: '#666', marginBottom: '1rem' }}>
          Welcome, {user || 'User'}!
        </p>
        <p style={{ color: '#666', fontSize: '0.9rem' }}>
          You have successfully registered and logged in.
        </p>
        
        <div style={{ marginTop: '2rem' }}>
          <button 
            onClick={handleLogout}
            style={{ 
              maxWidth: '200px',
              padding: '0.75rem 1.5rem',
              backgroundColor: '#e74c3c',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

export default SuccessPage;
