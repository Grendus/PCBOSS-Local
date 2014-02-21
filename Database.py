import sqlite3
from datetime import datetime

dbname = "localdb.db"

#checks the validity of every username/password combo
def isValid(uname, pwd):
    conn = sqlite3.connect(dbname) 
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE email_address=? and password=?", (uname, pwd));
    userExists = c.fetchone() != None
    conn.close()
    return userExists

#returns a list of dictionaries. Each one should have a filename, upload time, description, and status
def getJobs(uname):
    filelist = []
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("SELECT time, filename, description, status FROM CADFile WHERE submitter_name = ?", (uname,))
    for stored_file in c.fetchmany():
        filepoint={}
        filepoint['time'] = stored_file.time
        filepoint['name'] = stored_file.filename
        filepoint['description'] = stored_file.description
        filepoint['status'] = stored_file.status
        filelist.append(filepoint)
    conn.close()
    return filelist

def getUserInfo(uname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("select email_address, first_name, last_name from user WHERE email_address = ?", (uname,))
    try:
        userData = c.fetchone()
        userDict = {"email":userData[0],
                    "fname":userData[1],
                    "lname":userData[2]}
    except AttributeError:
        userDict = {"email":"invalid", "fname":'invalid', 'lname':'invalid'}

    conn.close()
    return userDict

#stores a file in the datastore
def storeFile(ID, encFile, filedesc):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    uploadedFile = {"submitter_name":ID,
                    "filename":encFile[0]['filename'],
                    "time":datetime.now(),
                    "description":filedesc,
                    "status":"Pending",
                    "CADFile":encFile[0]['body']}
    
    c.execute("insert into CADFile values (:submitter_name,:filename,:CADFile,:time,:status,:description)", uploadedFile)
    c.commit()
    conn.close()

#adds a user to the system; should only be done by the home system
def addUser(email, encpwd, fname, lname):
    try:
        newUser = user(email_address=email,
                       password=encpwd,
                       first_name=fname,
                       last_name=lname)
        newUser.put()
    except:
        return False
    return True

def updateAccount(email, fname, lname, pword=False):
    selectedUser = user.gql("WHERE email_address = :1", email).get()
    if pword:
        selectedUser.password = pword
    selectedUser.first_name = fname
    selectedUser.last_name = lname
    selectedUser.put()

def listJobs():
    jobs = CADFile.gql('')
    joblist = []
    for job in jobs:
        jobdict = job.export()
        del jobdict["CADFile"]
        joblist.append(jobdict)
    return joblist

def getJob(filenum):
    #todo: fix the GQL injection vulnerability here. Probably safe, it's behind an authorization wall, but still bad form to leave it there
    job = CADFile.gql("WHERE __key__ = KEY('CADFile', "+str(filenum)+")").get()
    return job.export()

def updateStatus(filenum, status):
    job = getJob(filenum)
    job.status = status
    job.put()

def mostRecentFile():
    job = CADFile.gql("ORDER BY time DESC LIMIT 1").get()
    return job.export()

def mostRecentTimestamp():
    return mostRecentFile().time

def listUsers():
    users = user.gql("")
    userlist = []
    for userinfo in users:
        userlist.append(userinfo.email_address)
    return userlist
