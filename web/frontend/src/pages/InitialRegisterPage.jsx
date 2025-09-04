import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '../services/api';

function InitialRegisterPage() {
  const videoRef = useRef(null);
  const photoRef = useRef(null);
  const streamRef = useRef(null);
  const [hasPhoto, setHasPhoto] = useState(false);
  const [userId, setUserId] = useState('');
  const [name, setName] = useState('');
  const [loginKey, setLoginKey] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const navigate = useNavigate();

  const startCamera = () => {
    navigator.mediaDevices.getUserMedia({
      video: { width: 300, height: 300 }
    })
    .then(stream => {
      streamRef.current = stream;
      let video = videoRef.current;
      video.srcObject = stream;
      video.play();
      setIsCameraOn(true);
    })
    .catch(err => {
      console.error(err);
      setError("Could not access webcam. Please ensure it's connected and permissions are granted.");
    });
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      let video = videoRef.current;
      video.srcObject = null;
      setIsCameraOn(false);
    }
  };

  const takePhoto = () => {
    const width = 300;
    const height = 300;
    let video = videoRef.current;
    let photo = photoRef.current;

    photo.width = width;
    photo.height = height;

    let ctx = photo.getContext('2d');
    ctx.drawImage(video, 0, 0, width, height);
    setHasPhoto(true);
  };

  const clearPhoto = () => {
    let photo = photoRef.current;
    let ctx = photo.getContext('2d');
    ctx.clearRect(0, 0, photo.width, photo.height);
    setHasPhoto(false);
  };

  const handleRegister = async () => {
    setError('');
    setMessage('');
    if (!userId || !name || !loginKey) {
      setError("All fields are required.");
      return;
    }
    if (!hasPhoto) {
      setError("Please take a photo for face recognition.");
      return;
    }

    setLoading(true);
    let photo = photoRef.current;
    photo.toBlob(async (blob) => {
      try {
        const userData = { user_id: userId, name, login_key: loginKey, role: 'admin' }; // Role is always admin
        const response = await registerUser(userData, blob);
        setMessage(response.message);
        setUserId('');
        setName('');
        setLoginKey('');
        setHasPhoto(false);
        clearPhoto();
        // Navigate to login page after successful registration
        navigate('/login');
      } catch (err) {
        setError(err.detail || err || "Registration failed.");
        console.error("Registration error:", err);
      } finally {
        setLoading(false);
      }
    }, 'image/jpeg');
  };

  return (
    <div>
      <h2>Initial Admin Registration</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {loading && <p>Processing...</p>}
      <div>
        <input
          type="text"
          placeholder="User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          disabled={loading}
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={loading}
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="Login Key"
          value={loginKey}
          onChange={(e) => setLoginKey(e.target.value)}
          disabled={loading}
        />
      </div>
      <p>Role: Admin (fixed for initial registration)</p>
      <div className="camera">
        <video ref={videoRef}></video>
        <button onClick={startCamera} disabled={loading || isCameraOn}>Start Camera</button>
        <button onClick={stopCamera} disabled={loading || !isCameraOn}>Stop Camera</button>
        <button onClick={takePhoto} disabled={loading || !isCameraOn}>Take Photo</button>
      </div>
      <div className={'result' + (hasPhoto ? ' hasPhoto' : '')}>
        <canvas ref={photoRef}></canvas>
        <button onClick={clearPhoto} disabled={loading}>Clear Photo</button>
      </div>
      <button onClick={handleRegister} disabled={loading}>Register Admin</button>
    </div>
  );
}

export default InitialRegisterPage;