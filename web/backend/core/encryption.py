import uuid
import hashlib

class EncryptionHandler:
    def generate_salt(self):
        return uuid.uuid4().hex

    def hash_key(self, key, salt):
        return hashlib.sha256((key + salt).encode()).hexdigest()

    def verify_key(self, input_key, stored_hash, salt):
        return self.hash_key(input_key, salt) == stored_hash
