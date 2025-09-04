import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Replace with your FastAPI backend URL

const api = axios.create({
  baseURL: API_URL,
});

export const registerUser = async (userData, faceImage) => {
  const formData = new FormData();
  formData.append('user_id', userData.user_id);
  formData.append('name', userData.name);
  formData.append('login_key', userData.login_key);
  formData.append('role', userData.role || 'normal');
  formData.append('face_image', faceImage);

  try {
    const response = await api.post('/register', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const loginUser = async (loginKey, faceImage) => {
  const formData = new FormData();
  formData.append('login_key', loginKey);
  formData.append('face_image', faceImage);

  try {
    const response = await api.post('/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getUserProfile = async (userId) => {
  try {
    const response = await api.get(`/profile/${userId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getAllUsers = async () => {
  try {
    const response = await api.get('/users');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const changeLoginKey = async (oldLoginKey, newLoginKey) => {
  try {
    const response = await api.post('/change-login-key', { old_login_key: oldLoginKey, new_login_key: newLoginKey });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const deleteUser = async (userId) => {
  try {
    const response = await api.delete(`/delete-user/${userId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getStorageInfo = async () => {
  try {
    const response = await api.get('/storage-info');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const isDbEmpty = async () => {
  try {
    const response = await api.get('/is-db-empty');
    return response.data.is_empty;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};