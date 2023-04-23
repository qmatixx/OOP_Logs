import re
from Journal import SSHLogJournal
from parse_log import parse_ssh_log
from LogEntries import *
from Journal import SSHLogJournal
from Utils import *

class SSHUser:
    def __init__(self, username, last_login_date):
        self.username = username
        self.last_login_date = last_login_date
        
    def validate(self):
        print("Validating user: ", self.username)
        pattern = r'^[a-z_][a-z0-9_-]{0,31}$'
        match = re.match(pattern, self.username)
        if match:
            return True
        return False
    
if __name__ == '__main__':
    journal = SSHLogJournal()
    with open("logs.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            journal.append(line)
    users = []
    for entry in journal:
        username = get_user_from_log(entry.message)
        time = entry.timestamp
        user = SSHUser(username, time)
        if user.username in [u.username for u in users]:
            for u in users:
                if u.username == user.username:
                    u.last_login_date = user.last_login_date
        elif user.username != None:
            users.append(user)
    for user in users:
        print(user.username, user.last_login_date)
        
    # zip journal and users
    list = journal.logList + users
    for sth in list:
        sth.validate()
    
    
        