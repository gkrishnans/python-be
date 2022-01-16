from database import mydb

def create_user(data):
    mydb["User"].insert_one(data)


def create_group(data):
    mydb["Group"].insert_one(data)
