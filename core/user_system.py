from core.face_data import FaceData
from core.encryption import EncryptionHandler
from core.storage import StorageHandler
from deepface import DeepFace
import base64
import cv2
import numpy as np

class UserSystem:
    def __init__(self):
        self.storage = StorageHandler()
        self.encryption = EncryptionHandler()
        self.face_data = FaceData()
        self.logged_in_user = None

    def is_db_empty(self):
        return self.storage.is_collection_empty()

    def get_storage_info(self):
        return self.storage.get_collection_stats()

    def register_user(self, user_id, login_key, role="normal", name=""):
        if not user_id or not login_key:
            print("[ERROR] User ID and Login Key cannot be empty.")
            return False

        # Check if user_id already exists
        if self.storage.load_user(user_id):
            print(f"[ERROR] User with ID '{user_id}' already exists.")
            return False

        frames = self.face_data.capture_multiple_faces()

        if not frames:
            print("[ERROR] No face data captured for registration.")
            return False

        encoded_frames = []
        for frame in frames:
            _, buffer = cv2.imencode('.jpg', frame)
            encoded_frames.append(base64.b64encode(buffer).decode('utf-8'))

        salt = self.encryption.generate_salt()
        hashed_key = self.encryption.hash_key(login_key, salt)

        user_profile = {
            "user_id": user_id,
            "name": name,
            "hashed_key": hashed_key,
            "salt": salt,
            "frames": encoded_frames,
            "role": role
        }

        self.storage.save_user(user_profile)
        print(f"[INFO] User {user_id} registered successfully.")
        return True

    def login_user(self, login_key):
        if not login_key:
            print("[ERROR] Login Key cannot be empty.")
            return False
        
        live_frames = self.face_data.capture_multiple_faces(num_images=1, require_liveness=True)

        if not live_frames:
            print("[ERROR] No face data captured for login.")
            return False

        users = self.storage.load_users()
        live_frame = live_frames[0]

        for user in users:
            face_matched = False
            if 'frames' in user and user['frames']:
                for encoded_ref_frame in user['frames']:
                    try:
                        decoded_frame = base64.b64decode(encoded_ref_frame)
                        np_arr = np.frombuffer(decoded_frame, np.uint8)
                        ref_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                        
                        result = DeepFace.verify(img1_path=live_frame, img2_path=ref_frame, model_name="VGG-Face", enforce_detection=False)
                        if result['verified']:
                            face_matched = True
                            break
                    except Exception as e:
                        print(f"[ERROR] DeepFace verification failed: {e}")
                        continue
            elif 'embeddings' in user and user['embeddings']:
                print("[WARNING] User has old embedding data. Face verification will be insecure. Please re-register for enhanced security.")
                try:
                    live_embedding = DeepFace.represent(img_path=live_frame, model_name='VGG-Face', enforce_detection=False)[0]['embedding']
                    for ref_embedding in user['embeddings']:
                        distance = sum((a - b) ** 2 for a, b in zip(live_embedding, ref_embedding)) ** 0.5
                        if distance < 0.6:
                            face_matched = True
                            break
                except Exception as e:
                    print(f"[ERROR] Embedding comparison failed: {e}")
                    continue

            if face_matched:
                if self.encryption.verify_key(login_key, user['hashed_key'], user['salt']):
                    self.logged_in_user = {"user_id": user['user_id'], "role": user.get('role', 'normal'), "name": user.get('name', '')}
                    
                    # Record login timestamp
                    import datetime
                    self.storage.add_login_timestamp(user['user_id'], datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))

                    print(f"[INFO] User {user['user_id']} logged in successfully.")
                    return self.logged_in_user
        
        print("[INFO] Login failed: Face or key mismatch.")
        return None

    def logout_user(self):
        self.logged_in_user = None
        print("[INFO] User logged out.")

    def get_logged_in_user(self):
        return self.logged_in_user

    def get_all_users(self):
        return self.storage.load_users()

    def get_user_login_timestamps(self, user_id):
        user = self.storage.load_user(user_id)
        if user and 'login_timestamps' in user:
            return user['login_timestamps']
        return []

    def change_login_key(self, user_id, old_login_key, new_login_key):
        user = self.storage.load_user(user_id)
        if not user:
            print(f"[ERROR] User {user_id} not found.")
            return False

        if not self.encryption.verify_key(old_login_key, user['hashed_key'], user['salt']):
            print("[ERROR] Old login key is incorrect.")
            return False

        new_salt = self.encryption.generate_salt()
        new_hashed_key = self.encryption.hash_key(new_login_key, new_salt)

        user['hashed_key'] = new_hashed_key
        user['salt'] = new_salt
        self.storage.update_user(user)
        print(f"[INFO] Login key for user {user_id} changed successfully.")
        return True

    def delete_user(self, user_id):
        return self.storage.delete_user(user_id)