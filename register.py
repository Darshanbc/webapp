import hashlib,dbops,app
from cryptography.fernet import Fernet

class twoWordHash:
    
    def __init__(self,word1,word2):
        self.conVar=hashlib.sha256()
        self.word1=str(word1)
        self.word2=str(word2)

    def getHash(self):
        print str(self.word1+self.word2)
        self.conVar.update(self.word1+self.word2)
        return self.conVar.hexdigest()

def authcreds(empid,password):
    # phash=hashlib.sha256()
    hashobj=twoWordHash(empid,password)
    Hash=hashobj.getHash()
    print "hash ="+str(Hash)
    dbconnobj=dbops.dbConn()
    dbconnobj.operation('login')
    result=dbconnobj.loginQuery(empid)
    if result.count()==1 and result.next()["PassHash"]==Hash:
            return True
    else:
            return False


def signup(attr):
    dbconnobj=dbops.dbConn()
    dbconnobj.operation("signup")
    attr["key"]=Fernet.generate_key()
    result=dbconnobj.loginQuery(attr['uname'])
    if result.count()==0:
        dbconnobj.insert(attr)
        return "Signup Successful"
    else:
        return "User ID already exists"
