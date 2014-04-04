import random
import keys
import Crypto.PublicKey.RSA
import base64

encryption_key = Crypto.PublicKey.RSA.importKey(keys.public_key)
decryption_key = Crypto.PublicKey.RSA.importKey(keys.private_key)

def pwdHash(pwd):
    #todo: add hash function
    return encryption_key.sign(pwd)

def sessionToken():
    #todo: implement secure session ID generator
    sessionToken=""
    for x in range(16):
        sessionToken+=str(random.randint(0,9))
    return sessionToken

"""
Messages can contain three different classes of value: dictionaries, lists, or values that 
can be cast to string. This recursively parses the message, encrypting each part of the message
while leaving the structure intact.
"""

def encryptFile(unencryptedFile):
    #todo: add encryption
    return base64.encodestring(encryption_key.encrypt(str(unencryptedFile), None)[0])

def encryptDict(unencryptedDict):
	encryptedDict = dict()
	for key, value in unencryptedDict.iteritems():
		encryptedDict[encrypt(key)] = encrypt(value)
	return encryptedDict

def encryptList(unencryptedList):
	encryptedList = list()
	for value in unencryptedList:
		encryptedList.append(encrypt(value))
	return encryptedList

def encrypt(unencryptedMessage):
	if type(unencryptedMessage) is dict:
		return encryptDict(unencryptedMessage)
	elif type(unencryptedMessage) is list:
		return encryptList(unencryptedMessage)
	else:
		return encryptFile(unencryptedMessage)

"""
Same as above, recursively decrypt the message sent. The logic is the same on both the
server and local system, just different keys.
"""

def decryptFile(encryptedFile):
	return decryption_key.decrypt(base64.decodestring(encryptedFile))

def decryptDict(encryptedDict):
	decryptedDict = dict()
	for key, value in encryptedDict.iteritems():
		decryptedDict[decrypt(key)] = decrypt(value)
	return decryptedDict

def decryptList(encryptedList):
	decryptedList = list()
	for value in encryptedList:
		decryptedList.append(decrypt(value))
	return decryptedList

def decrypt(encryptedMessage):
	if type(encryptedMessage) is dict:
		return decryptDict(encryptedMessage)
	elif type(encryptedMessage) is list:
		return decryptList(encryptedMessage)
	else:
		return decryptFile(encryptedMessage)
