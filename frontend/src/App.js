import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import SuccessPage from './components/SuccessPage';

function App() {
  const [isLogin, setIsLogin] = useState(true);

  const handleToggleForm = () => {
    setIsLogin(!isLogin);
  };

  const handleLoginSuccess = (data) => {
    console.log('Login successful:', data);
  };

  const handleRegisterSuccess = (data) => {
    console.log('Register successful:', data);
  };

  // Roteamento baseado no pathname
  if (window.location.pathname === '/success') {
    return <SuccessPage />;
  }

  return (
    <div>
      {isLogin ? (
        <Login 
          onToggleForm={handleToggleForm}
          onLoginSuccess={handleLoginSuccess}
        />
      ) : (
        <Register 
          onToggleForm={handleToggleForm}
          onRegisterSuccess={handleRegisterSuccess}
        />
      )}
    </div>
  );
}

export default App;
