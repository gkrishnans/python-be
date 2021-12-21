from database import mydb

def update_user(query,data):
    mydb["User"].update_one(
        query,
        {
            "$set": data
        }
    )

