import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { changeLoginKey } from '../services/api';

function ChangeLoginKeyPage() {
  const [oldLoginKey, setOldLoginKey] = useState('');
  const [newLoginKey, setNewLoginKey] = useState('');
  const [confirmNewLoginKey, setConfirmNewLoginKey] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChangeLoginKey = async () => {
    setError('');
    setMessage('');
    if (!oldLoginKey || !newLoginKey || !confirmNewLoginKey) {
      setError("All fields are required.");
      return;
    }
    if (newLoginKey !== confirmNewLoginKey) {
      setError("New login key and confirmation do not match.");
      return;
    }

    setLoading(true);
    try {
      await changeLoginKey(oldLoginKey, newLoginKey);
      setMessage("Login key changed successfully!");
      setOldLoginKey('');
      setNewLoginKey('');
      setConfirmNewLoginKey('');
      // Optionally navigate back to user dashboard after successful change
      navigate('/user-dashboard');
    } catch (err) {
      setError(err.detail || err || "Failed to change login key.");
      console.error("Change login key error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Change Login Key</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {loading && <p>Processing...</p>}
      <div>
        <input
          type="password"
          placeholder="Old Login Key"
          value={oldLoginKey}
          onChange={(e) => setOldLoginKey(e.target.value)}
          disabled={loading}
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="New Login Key"
          value={newLoginKey}
          onChange={(e) => setNewLoginKey(e.target.value)}
          disabled={loading}
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="Confirm New Login Key"
          value={confirmNewLoginKey}
          onChange={(e) => setConfirmNewLoginKey(e.target.value)}
          disabled={loading}
        />
      </div>
      <button onClick={handleChangeLoginKey} disabled={loading}>Change Key</button>
      <button onClick={() => navigate('/user-dashboard')} disabled={loading}>Back to Dashboard</button>
    </div>
  );
}

export default ChangeLoginKeyPage;