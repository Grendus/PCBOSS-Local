import Encryption
import Database


#since we only expect to have a few users at any given time, we can cache the valid tokens and save on datastore access
#todo: tokens should expire at some point. Valid workaround involves restarting the server daily
validTokens = {}

def authUser(uname, pwd):
    pwdHash = Encryption.pwdHash(pwd)
    if Database.isValid(uname,pwdHash):
        token = Encryption.sessionToken()

        #It's almost impossibly unlikely that we'll wind up with two identical tokens,
        #but if we did, it would be a hard bug to find.
        while token in validTokens:
            token = Encryption.sessionToken()
        validTokens[token] = uname
        return token
    return False

def validateUser(token):
    return token in validTokens

def authViewRequest(token):
    if token in validTokens:
        return Database.getJobs(validTokens[token])

def authUpload(ID, CADFile, filedesc):
    #todo: figure out how to authenticate the file
    encFile = Encryption.encryptFile(CADFile)
    Database.storeFile(ID, encFile, filedesc)
