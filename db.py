from pymongo import MongoClient

class Database:
    client = MongoClient('mongodb://localhost:27017')
    db = client['IVOverflow']

    @staticmethod
    def get_db():
        return Database.db
