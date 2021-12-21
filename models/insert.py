from database import mydb

def create_user(data):
    mydb["User"].insert_one(data)

