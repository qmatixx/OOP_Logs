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
        pattern = r'^[a-z_][a-z0-9_-]{0,31}$'
        match = re.match(pattern, self.username)
        if match:
            return True
        return False
    
if __name__ == '__main__':
    with open("logs.txt", 'r') as f:
        logs = []
        lines = f.readlines()
        for line in lines:
            logs.append(SSHLogEntry(line))    
    journal = SSHLogJournal(logs)
    user_list = []
    for entry in journal:
        username = get_user_from_log(entry.message)
        last_login = entry.timestamp
        user = SSHUser(username, last_login)
        if user not in user_list:
            user_list.append(user)
    list = zip(journal.logList, user_list)
    for sth in list:
        sth.validate()
    
    
        