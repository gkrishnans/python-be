
from database import mydb

def getData(query):
    try:
        data = mydb["User"].find_one(query)
        if(data == None):
            return []
        return list(data)
    except Exception as error:
        print(str(error))
        return []


