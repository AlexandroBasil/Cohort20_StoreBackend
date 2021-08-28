from config import db

#  test for database access

# db.users.insert_one({"name": "Basil", "email": "ag@mongo.com"})
# db.users.insert_one({"name": "Admin", "email": "admin@mongo.com"})
# db.users.insert_one({"name": "Staff", "email": "staff@mongo.com"})


cursor = db.users.find({ "name": "Staff"})
for user in cursor:
    print(user)