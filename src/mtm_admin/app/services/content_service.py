import os
import pymongo

class ComtentService:
    
    def __init__(self):
        self.connection_string = os.environ.get("COSMOS_DB_CONNECTION_STRING")
        self.db_name = os.environ.get("COSMOS_DB_NAME")
        self.collection_name = os.environ.get("COSMOS_DB_COLLECTION_NAME")

    def get_all_modules(self):
        client = pymongo.MongoClient(self.connection_string)
        collection = self.get_collection(client=client)
    
        modules = collection.find()
    
        return modules
    
    def get_collection(self, client):
        db = client[self.db_name]
        collection = db[self.collection_name]
        return collection