import sqlite3
import datetime, time

dbname = "localdb.sqlite"
sqlite3.register_adapter(datetime.datetime, lambda x: time.mktime(x.timetuple()))

#checks the validity of every username/password combo
def isValid(uname, pwd):
    conn = sqlite3.connect(dbname) 
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE email_address=? and password=?", (uname, pwd));
    userExists = c.fetchone() != None
    conn.commit()
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
        #splittime = stored_file[0].split("-")
        filepoint['time'] = datetime.datetime.fromtimestamp(stored_file[0])
        filepoint['name'] = stored_file[1]
        filepoint['description'] = stored_file[2]
        filepoint['status'] = stored_file[3]
        filelist.append(filepoint)
    conn.commit()
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
    conn.commit()
    conn.close()
    return userDict

#stores a file in the datastore
def storeFile(ID, encFile, filedesc):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    uploadedFile = {"submitter_name":ID,
                    "filename":encFile[0]['filename'],
                    "time":datetime.datetime.now(),
                    "description":filedesc,
                    "CADFile":encFile[0]['body'],
                    "status":"Pending"}
    
    c.execute("insert into CADFile values (:submitter_name,:filename,:time,:description,:CADFile,:status)", uploadedFile)
    conn.commit()
    conn.close()

#adds a user to the system; should only be done by the home system
def addUser(email, encpwd, fname, lname):
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("INSERT INTO user VALUES(?,?,?,?)",(email,encpwd,fname,lname))
    except Exception as e:
        print e
        return False
    finally:
        conn.commit()
        conn.close()
    return True

def updateAccount(email, fname, lname, pword=False):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    if pword:
        c.execute("UPDATE user SET password=?, first_name=?, last_name=? WHERE email_address=?",(pword,fname,lname,email))
    else:
        c.execute("UPDATE user SET first_name=?, last_name=? WHERE email_address=?",(fname,lname,email))
    conn.commit()
    conn.close()

def listJobs():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("SELECT submitter_name, filename, rowid, time, description, status from CADFile")
    jobs = c.fetchmany()
    joblist = []
    for job in jobs:
        jobdict = {"submitter_name":job[0],
                   "filename":job[1],
                   "key":job[2],
                   "time":datetime.datetime.fromtimestamp(job[3]),
                   "description":job[4],
                   "status":job[5]}
        joblist.append(jobdict)
    conn.commit()
    conn.close()
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
