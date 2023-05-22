import pymongo
from pymongo import MongoClient

uri = 'mongodb://127.0.0.1:27017'
client = MongoClient(uri,
                     username='root',
                     password='root',
                     authMechanism='SCRAM-SHA-256')

db = client["eshop"]
user_coll = db["users"]
new_user = {"username": "nina", "password": "xxx", "email": "123456@qq.com"}
# result = user_coll.insert_one(new_user)
# result

# result = user_coll.update_one({"username":"nina"}, {"$set":{"phone":"13927470636"}})
# print(result)

result = user_coll.find().limit(1)
print(result)
