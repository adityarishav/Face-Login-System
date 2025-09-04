import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserProfile } from '../services/api';

function UserDashboardPage() {
  const [userProfile, setUserProfile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserProfile = async () => {
      setLoading(true);
      try {
        const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
        if (!loggedInUser || !loggedInUser.user_id) {
          navigate('/login');
          return;
        }
        const data = await getUserProfile(loggedInUser.user_id);
        setUserProfile(data);
      } catch (err) {
        setError(err.detail || err || "Failed to fetch user profile.");
        console.error("Fetch user profile error:", err);
        navigate('/login'); 
      } finally {
        setLoading(false);
      }
    };
    fetchUserProfile();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('loggedInUser');
    navigate('/login');
  };

  if (loading || !userProfile) {
    return <div>Loading profile...</div>;
  }

  return (
    <div>
      <h2>User Dashboard</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <h3>User Profile</h3>
      <p><strong>Name:</strong> {userProfile.name}</p>
      <p><strong>User ID:</strong> {userProfile.user_id}</p>
      <p><strong>Role:</strong> {userProfile.role}</p>
      <p><strong>Last Login:</strong> {userProfile.last_login || 'N/A'}</p>
      <p><strong>Face Recognition Status:</strong> {userProfile.face_recognition_status}</p>

      <h3>Recent Logins</h3>
      {userProfile.recent_logins && userProfile.recent_logins.length > 0 ? (
        <ul>
          {userProfile.recent_logins.map((login, index) => (
            <li key={index}>{login}</li>
          ))}
        </ul>
      ) : (
        <p>No recent login activity.</p>
      )}

      <h3>Security Settings</h3>
      <button onClick={() => navigate('/change-login-key')} disabled={loading}>Change Login Key</button>

      <button onClick={handleLogout} disabled={loading}>Logout</button>
    </div>
  );
}

export default UserDashboardPage;