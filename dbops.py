import pymongo
import base64
import bson
from bson.binary import Binary
from urlparse import urlparse
import hashlib
import json

class dbConn:
    dbname = "testdb"
    def __init__(self):
        self.__operation=None

    def operation(self, operation):
        self.set_operation(operation)
        if self.get_operation() == 'signup' or self.get_operation() == 'login':
            self.set_collection("users")
        elif self.get_operation() == "insert_image":
                self.set_collection('images')

    def get_operation(self):
        return self.__operation
    def set_operation(self,operation):
        self.__operation=operation
    def get_collection(self):
        return self.__collection
    def set_collection(self,collection):
        self.__collection=collection

    def establishConnection(self):
        # establish a connection to the database
        uri = "mongodb://admin:admin123@127.0.0.1:27017"
        try:
            client = pymongo.MongoClient(uri)
            # client = self.establishConnection()
            db = client[self.__class__.dbname]
            coll = db[self.get_collection()]
            print("succesfully connected")
        except:
            print("Couldn't connect")
        return coll

    def insert(self, attr):
        coll=self.establishConnection() 
        try:
            coll.insert(attr)
            print "insertion succesful"
        except Exception as e:
            print e

    def loginQuery(self, uname):
        collection = self.establishConnection()
        result = collection.find({"uname": uname}, {"PassHash": 1})
        return result

    def query(self, queryString, Projection=None):
        coll=self.establishConnection()
        result = coll.find(queryString, Projection)
        return result
    
    def queryRecentAddedItem(queryString):
        coll=self.establishConnection()
        result= coll.coll.find().sort([('_id', -1)]).limit(1)
        resultDict= result.next()
        del resultDict["_id"]
        return resultDict
    #
    # def getKey(self, user):
    #     querystring = {"uname": user}
    #     projection = {"key": 1}
    #     return self.query(querystring, projection)
