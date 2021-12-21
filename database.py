from pymongo import MongoClient
myclient = MongoClient("mongodb+srv://gokul:gokul@pollotecluster.cru4v.mongodb.net/polloteCluster?retryWrites=true&w=majority")
mydb = myclient["christmas"]
print(mydb.list_collection_names())

