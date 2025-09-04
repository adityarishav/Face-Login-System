import React, { useEffect, useState, useRef } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'; // Import useLocation
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import UserDashboardPage from './pages/UserDashboardPage';
import AdminDashboardPage from './pages/AdminDashboardPage';
import InitialRegisterPage from './pages/InitialRegisterPage';
import AdminRegisterUserPage from './pages/AdminRegisterUserPage';
import ChangeLoginKeyPage from './pages/ChangeLoginKeyPage';
import ProtectedRoute from './components/ProtectedRoute';
import { isDbEmpty } from './services/api';

function App() {
  const [dbStatusChecked, setDbStatusChecked] = useState(false);
  const navigate = useNavigate();
  const location = useLocation(); // Get current location
  const initialCheckDone = useRef(false);
  const [loggedInUser, setLoggedInUser] = useState(null); 

  useEffect(() => {
    const handleStorageChange = () => {
      setLoggedInUser(JSON.parse(localStorage.getItem('loggedInUser')));
    };
    window.addEventListener('storage', handleStorageChange);
    handleStorageChange(); 

    if (initialCheckDone.current) {
      return;
    }

    const checkDbAndRedirect = async () => {
      try {
        const empty = await isDbEmpty();
        if (empty) {
          navigate('/initial-register');
        } else {
          const user = JSON.parse(localStorage.getItem('loggedInUser'));
          if (user) {
            if (user.role === 'admin') {
              navigate('/admin-dashboard');
            } else {
              navigate('/user-dashboard');
            }
          } else {
            navigate('/login');
          }
        }
      } catch (error) {
        console.error("Error checking DB status:", error);
        navigate('/login');
      } finally {
        setDbStatusChecked(true);
        initialCheckDone.current = true;
      }
    };

    checkDbAndRedirect();

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [navigate]);

  

  if (!dbStatusChecked) {
    return <div>Loading application...</div>;
  }

  return (
    <div className="App">
      

      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/initial-register" element={<InitialRegisterPage />} />
        
        <Route path="/user-dashboard" element={
          <ProtectedRoute allowedRoles={['normal', 'admin']}>
            <UserDashboardPage />
          </ProtectedRoute>
        } />
        <Route path="/admin-dashboard" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <AdminDashboardPage />
          </ProtectedRoute>
        } />
        <Route path="/admin-register-user" element={
          <ProtectedRoute allowedRoles={['admin']}>
            <AdminRegisterUserPage />
          </ProtectedRoute>
        } />
        <Route path="/change-login-key" element={
          <ProtectedRoute allowedRoles={['normal', 'admin']}>
            <ChangeLoginKeyPage />
          </ProtectedRoute>
        } />

        <Route path="/" element={null} />
      </Routes>
    </div>
  );
}

export default App;