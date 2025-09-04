from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
import os
import base64
import numpy as np
import cv2
import datetime

# Assuming core modules are accessible via PYTHONPATH or copied
# For now, let's assume they are in the same directory or properly imported
from core.user_system import UserSystem
from core.encryption import EncryptionHandler
from core.storage import StorageHandler
from core.face_data import FaceData

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173", # Vite React app default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core systems
user_system = UserSystem()
encryption_handler = EncryptionHandler()
storage_handler = StorageHandler()
face_data_handler = FaceData()

# --- Pydantic Models for Request/Response Bodies ---
class UserRegister(BaseModel):
    user_id: str
    name: str
    login_key: str
    role: Optional[str] = "normal"

class UserLogin(BaseModel):
    login_key: str
    # face_data: str # Base64 encoded image

class UserProfile(BaseModel):
    user_id: str
    name: str
    role: str
    last_login: Optional[str] = None
    face_recognition_status: str
    recent_logins: List[str]

class ChangeLoginKey(BaseModel):
    old_login_key: str
    new_login_key: str

class UserDelete(BaseModel):
    user_id: str

class StorageInfo(BaseModel):
    total_size_mb: float
    average_object_size_kb: float
    number_of_objects: int

# --- API Endpoints ---

@app.post("/register")
async def register_user(user_id: str = Form(...), name: str = Form(...), login_key: str = Form(...), role: Optional[str] = Form("normal"), face_image: UploadFile = File(...)):
    try:
        # Read image data
        image_data = await face_image.read()
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        success = user_system.register_user(
            user_id, login_key, frame, role, name
        )

        if success:
            return {"message": "User registered successfully!"}
        else:
            raise HTTPException(status_code=400, detail="Registration failed. User ID might already exist or face data capture failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error during registration: {e}")

@app.post("/login")
async def login_user(login_key: str = Form(...), face_image: UploadFile = File(...)):
    try:
        image_data = await face_image.read()
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        print(f"DEBUG: login_key type: {type(login_key)}, frame type: {type(frame)}")
        user_info = user_system.login_user(login_key, frame)

        if user_info:
            return {"message": "Login successful!", "user": user_info}
        else:
            raise HTTPException(status_code=401, detail="Login failed: Face not recognized or login key incorrect.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error during login: {e}")

@app.get("/profile/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str):
    user = user_system.get_logged_in_user() # In a real app, this would be based on authentication
    if not user or user['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Access denied or user not logged in.")

    # Get last login
    timestamps = user_system.get_user_login_timestamps(user_id)
    last_login = sorted(timestamps, reverse=True)[0] if timestamps else None

    # Determine face recognition status
    face_data_exists = False
    all_users_data = storage_handler.load_users() # Load all users to check for face data
    for u in all_users_data:
        if u.get('user_id') == user_id:
            if u.get('frames') and len(u.get('frames')) > 0:
                face_data_exists = True
            break

    return UserProfile(
        user_id=user['user_id'],
        name=user['name'],
        role=user['role'],
        last_login=last_login,
        face_recognition_status="Active" if face_data_exists else "Inactive",
        recent_logins=sorted(timestamps, reverse=True) # All timestamps for recent logins
    )

@app.get("/users", response_model=List[UserProfile])
async def get_all_users():
    current_user = user_system.get_logged_in_user()
    if not current_user or current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Access denied: Admin privileges required.")

    users_data = user_system.get_all_users()
    response_users = []
    for user in users_data:
        timestamps = user_system.get_user_login_timestamps(user['user_id'])
        last_login = sorted(timestamps, reverse=True)[0] if timestamps else None

        face_data_exists = False
        if user.get('frames') and len(user.get('frames')) > 0:
            face_data_exists = True

        response_users.append(UserProfile(
            user_id=user['user_id'],
            name=user['name'],
            role=user['role'],
            last_login=last_login,
            face_recognition_status="Active" if face_data_exists else "Inactive",
            recent_logins=sorted(timestamps, reverse=True) # All timestamps for recent logins
        ))
    return response_users

@app.post("/change-login-key")
async def change_login_key(change_key: ChangeLoginKey):
    current_user = user_system.get_logged_in_user()
    if not current_user:
        raise HTTPException(status_code=401, detail="Not logged in.")

    success = user_system.change_login_key(
        current_user['user_id'], change_key.old_login_key, change_key.new_login_key
    )

    if success:
        return {"message": "Login key changed successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Failed to change login key. Old key might be incorrect.")

@app.delete("/delete-user/{user_id}")
async def delete_user(user_id: str):
    current_user = user_system.get_logged_in_user()
    if not current_user or current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Access denied: Admin privileges required.")

    success = user_system.delete_user(user_id)
    if success:
        return {"message": f"User {user_id} deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found or failed to delete.")

@app.get("/storage-info", response_model=StorageInfo)
async def get_storage_info():
    stats = user_system.get_storage_info()
    if stats:
        return StorageInfo(
            total_size_mb=stats['size'] / (1024*1024),
            average_object_size_kb=stats['avgObjSize'] / 1024,
            number_of_objects=stats['count']
        )
    else:
        raise HTTPException(status_code=500, detail="Could not retrieve storage information.")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Face Recognition API"}

@app.get("/is-db-empty")
async def is_db_empty():
    return {"is_empty": user_system.is_db_empty()}

# You might need to add CORS middleware for frontend to communicate
# from fastapi.middleware.cors import CORSMiddleware
# origins = [
#     "http://localhost:3000", # React app default port
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )