import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAllUsers, deleteUser, getStorageInfo } from '../services/api';

function AdminDashboardPage() {
  const [users, setUsers] = useState([]);
  const [storageInfo, setStorageInfo] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchUsersAndStorage = async () => {
    setLoading(true);
    try {
      const usersData = await getAllUsers();
      setUsers(usersData);

      const info = await getStorageInfo();
      setStorageInfo(info);
    } catch (err) {
      setError(err.detail || err || "Failed to fetch data.");
      console.error("Admin dashboard fetch error:", err);
      if (err && err.detail && err.detail.includes("Admin privileges required")) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsersAndStorage();
  }, []);

  const handleDeleteUser = async (userId) => {
    if (window.confirm(`Are you sure you want to delete user ${userId}?`)) {
      setLoading(true);
      try {
        const response = await deleteUser(userId);
        setMessage(response.message);
        fetchUsersAndStorage(); // Refresh list
      } catch (err) {
        setError(err.detail || err || "Failed to delete user.");
        console.error("Delete user error:", err);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('loggedInUser');
    navigate('/login');
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {loading && <p>Processing...</p>}

      <h3>Admin Actions</h3>
      <button onClick={() => navigate('/admin-register-user')} disabled={loading}>Register New User</button>
      <button onClick={() => navigate('/change-login-key')} disabled={loading}>Change Login Key</button>

      <h3>All Users</h3>
      {users.length > 0 ? (
        <ul>
          {users.map(user => (
            <li key={user.user_id}>
              {user.name} ({user.user_id}) - Role: {user.role} - Last Login: {user.last_login || 'N/A'}
              <button onClick={() => handleDeleteUser(user.user_id)} disabled={loading}>Delete</button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No users registered.</p>
      )}

      <h3>Recent Logins (All Users)</h3>
      {users.some(user => user.recent_logins && user.recent_logins.length > 0) ? (
        <ul>
          {users.flatMap(user => 
            user.recent_logins ? user.recent_logins.map((login, index) => 
              <li key={`${user.user_id}-${index}`}>User {user.user_id}: {login}</li>
            ) : []
          ).sort().slice(-4).reverse().map((item, index) => <li key={index}>{item}</li>)}
        </ul>
      ) : (
        <p>No recent login activity for any user.</p>
      )}

      <h3>Storage Information</h3>
      {storageInfo ? (
        <div>
          <p>Total Size: {storageInfo.total_size_mb.toFixed(2)} MB</p>
          <p>Average Object Size: {storageInfo.average_object_size_kb.toFixed(2)} KB</p>
          <p>Number of Objects: {storageInfo.number_of_objects}</p>
        </div>
      ) : (
        <p>Could not retrieve storage information.</p>
      )}

      <button onClick={handleLogout} disabled={loading}>Logout</button>
    </div>
  );
}

export default AdminDashboardPage;