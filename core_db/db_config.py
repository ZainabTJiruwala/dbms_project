
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"

def get_db():
    client = MongoClient(MONGO_URI)
    return client["GeneVaultDB"]