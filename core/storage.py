from pymongo import MongoClient
import urllib.parse 

class StorageHandler:
    def __init__(self):
        # It is highly recommended to secure your MongoDB instance.
        # For production, use authentication, authorization, and network encryption (SSL/TLS).
        # Example with authentication: MongoClient('mongodb://user:pass@localhost:27017/')
        # self.client = MongoClient('mongodb+srv://todoapp:adityA10@cluster0.2u9rf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        self.client = MongoClient('mongodb://localhost:27017/') 
        self.db = self.client['face_login_db_vgg']
        self.users_collection = self.db['users']
    def save_user(self, user_data):
        self.users_collection.insert_one(user_data)

    def load_users(self):
        return list(self.users_collection.find({}))

    def is_collection_empty(self):
        return self.users_collection.count_documents({}) == 0

    def get_collection_stats(self):
        return self.db.command("collstats", "users")

    def delete_all_users(self):
        self.users_collection.delete_many({})

    def load_user(self, user_id):
        return self.users_collection.find_one({"user_id": user_id})

    def update_user(self, user_data):
        self.users_collection.update_one({"user_id": user_data['user_id']}, {"$set": user_data})

    def add_login_timestamp(self, user_id, timestamp):
        self.users_collection.update_one(
            {"user_id": user_id},
            {"$push": {"login_timestamps": {"$each": [timestamp], "$slice": -4}}}
        )

    def delete_user(self, user_id):
        result = self.users_collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0

    def close_connection(self):
        self.client.close()