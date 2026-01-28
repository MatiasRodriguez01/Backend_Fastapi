from pymongo import MongoClient

db_client = MongoClient().local

collection = db_client.users_test