
#Imports
from os import pathsep
import re
import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth
from flask import Flask, request,jsonify
from models.insert import create_group, create_user
from models.select import getData
from models.update import update_user
#App configuration
app = Flask(__name__)
#Connect to firebase
cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
#firebase = pyrebase.initialize_app(config)
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))
#Data source
users = [{'uid': 1, 'name': 'Noah Schairer'}]
#Api route to get users

#checking whether a new user or an existing user
@app.route('/signer',methods = ['post'])
def signer():
    try:
        request_data = request.get_json()
        phoneNumber = request_data['phoneNumber']
        newUser = getData({'phoneNumber':phoneNumber})
        if(newUser == []):
            message = "new user"
            newUser = True
        else:
            print(newUser)
            message = "already existing"
            newUser = False
        return jsonify({"message":message,'newUser':newUser}), 201
    except Exception as error:
        return jsonify({'debug_message':str(error)}), 424

def getAllUsers():
    users = []
    for user in auth.list_users().iterate_all():
        users.append(user.phone_number)
        print(user)
    return users


#a method get all common users
@app.route('/getCommonUsers',methods = ['post'])
def getCommonUsers():
    request_data = request.get_json()
    contactList = request_data['contactList']
    allUsers = getAllUsers()
    commonUsers = list(set(allUsers).intersection(set(contactList)))
    return jsonify({'commonUsers':commonUsers}), 200


#after firebase authentication api should be called
@app.route('/createUser',methods = ['post'])
def createUser():
    try:
        request_data = request.get_json()
        phoneNumber = request_data['phoneNumber']
        deviceToken = request_data['deviceToken']
        uid = request_data['uid']
        data = {
            "phoneNumber" : phoneNumber,
            "deviceToken" : deviceToken,
            "uid" : uid,
            "name":"",
            "profile-url":""
        }
        create_user(data)
        return jsonify({'message':"User created successfully"}), 201
    except Exception as error:
        return jsonify({'debug_message':str(error),"message":"Error occured in creating user"}), 424

#update the user profile
@app.route('/updateUser',methods = ['post'])
def updateUser():
    try:
        request_data = request.get_json()
        name = request_data['name']
        phoneNumber = request_data['phoneNumber']
        query = {
            "phoneNumber":phoneNumber
        }
        data = {
            "name" : name,
            "profile-url" : "profile-s3-link"
        }
        update_user(query,data)
        return jsonify({'message':"User updated successfully"}), 201
    except Exception as error:
        return jsonify({'debug_message':str(error),"message":"Error occured in updating user"}), 424

# {
# name:'Qa group',
# startDate:'10-12-2021',
# endDate:'20-12-2021'
# }



#creating group
@app.route('/createGroup',methods = ['post'])
def createGroup():
    try:
        request_data = request.get_json()
        groupName = request_data['groupName']
        startDate = request_data['startDate']
        endDate = request_data['endDate']
        creatorName = request_data['creatorName']
        participants = request_data['participants']
        data = {
            "groupName" : groupName,
            "startDate" : startDate,
            "endDate" : endDate,
            "groupID":"groupid",
            "participants":"getParticipantsDetails(participants)",
            "createdBy":creatorName
        }
        create_group(data)

        return jsonify({'message':"group created successfully"}), 201
    except Exception as error:
        return jsonify({'debug_message':str(error),"message":"Error occured in creating group"}), 424

def getParticipantsDetails(participants):
    participantsDetails = []
    for participant in participants:
        data = {
            participant:"getUserInfo"
        }
        participantsDetails.append(data)
    return participantsDetails

if __name__ == '__main__':
    app.run(debug=True)


# curl -X POST 127.0.0.1:5000/getCommonUsers -H "Content-Type: application/json" -d "{\
# "phoneNumber\":\"Read a book\",\"contactList\":\"hie\"}"




#curl -X POST 127.0.0.1:5000/getAllUsers -H "Content-Type: application/json" -d "{\"phoneNumber\":\"+919626671817\",\"s\":\"hie\"}"