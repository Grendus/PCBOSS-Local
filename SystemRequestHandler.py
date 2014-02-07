import tornado.web
import Database

"""
The PCBOSS printer system only has a single point of entry.
This helps secure the web server against malicious users by obfuscating
the entry point.

All requests must pass the following values:
auth = the authorization code todo: replace the easy to type authorization code with a hash
type = the type of request. Current accepted methods are "add_user", "list_jobs",
"request_files", "update_job_status", "recent_files", "get_users", "edit_user".

Requests of type "add_user" must pass the following values:
email = the email address or user name of the user being registered. The system will try
    to alert the user at this address, so if it isn't a valid email address the user will
    not be alerted.
password = the desired password todo: hash the passwords
first_name = the users first name. Something has to be passed, even if it's a dummy value.
last_name = the users last name. Something has to be passed, even if it's a dummy value.
"""

class SystemRequestHandler(tornado.web.RequestHandler):
    def post(self):
        if self.get_argument("auth")=="PCBOSS":
            requestType = self.get_argument("type")
            if requestType == "add_user":
                email = self.get_argument("email")
                password = self.get_argument("password")
                first_name = self.get_argument("first_name")
                last_name = self.get_argument("last_name")
                if Database.addUser(email, password, first_name, last_name):
                    self.write("Success")
                else:
                    self.write("Failure")
            elif requestType == "list_jobs":
                self.write(str(Database.listJobs()))
            elif requestType == "request_file":
                filenum = self.get_argument("file_number")
                self.write(str(Database.getJob(filenum).CADFile))
            elif requestType == "update_job_status":
                filenum = int(self.get_argument("file_number"))
                status = self.get_argument("status")
                Database.updateStatus(filenum, status)
            elif requestType == "recent_file":
                self.write(str(Database.mostRecentFile()))
            elif requestType == "recent_file_timestamp":
                self.write(str(Database.mostRecentTimestamp()))
            elif requestType == "get_users":
                self.write(str(Database.listUsers()))
            elif requestType == "edit_user":
                email = self.get_argument("email")
                fname = self.get_argument("first_name")
                lname = self.get_argument("last_name")
                pword = self.get_argument("password")
                Database.updateAccount(email, fname, lname, pword)
        else:
            self.write("Error: Unrecognized Request")

    def get(self):
        self.redirect("/")
            
