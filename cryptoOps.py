from cryptography.fernet import Fernet
import numpy as np
import pickle

class CryptoOps:

	def encrypt(self,data,key):
            self.data = data
            self.key = key
            bytedata = pickle.dumps(self.data)
            cryptosuite = Fernet(self.key)
            cipherText = cryptosuite.encrypt(bytedata)
            return cipherText
        def decrypt(self,key,data):
            self.key=key
            self.data=data
            cryptosuite=Fernet(self.key)
            byteData=cryptosuite.decrypt(self.data)
            return pickle.loads(byteData)
