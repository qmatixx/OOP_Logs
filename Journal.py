from Factory import *
from Utils import get_message_type
from datetime import datetime

class SSHLogJournal:

    def __init__(self, logList = []):
        self.logList = logList

    def __len__(self): return len(self.logList)

    def __iter__(self): return iter(self.logList)

    def __contains__(self, log):
        return log in self.logList
    
    def append(self, raw_log):
        factory_creator = self.get_creator(raw_log)
        sshEntry = factory_creator.create_sshLog(raw_log)
        if sshEntry.validate():
            self.logList.append(sshEntry)
            return True
        return False

    def get_creator(self, raw_log: str) -> Factory:
        type = get_message_type(raw_log)
        if type == "Authentication succeeded.":
            return Factory_Accepted_Pass()
        elif type == "Incorrect password.":
            return Factory_Failed_Pass()
        elif type == "Error.":
            return Factory_Error()
        else:
            return Factory_Other()
        
    def get_by_host(self, key_host=None):
        return [entry for entry in self.logList if entry.host == key_host]

    def get_by_timestamps(self, timestamp1, timestamp2):
        innerList = []
        for entry in self.logList:
            date = datetime.strptime(entry.timestamp,"%b %d %H:%M:%S")
            date_low = datetime.strptime(timestamp1,"%b %d %H:%M:%S")
            date_high = datetime.strptime(timestamp2,"%b %d %H:%M:%S")
            if date >= date_low and date <= date_high:
                innerList.append(entry)
        return innerList

        

if __name__ == "__main__":
    journal = SSHLogJournal()
    with open("logs.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            journal.append(line)
    filteredData = journal.get_by_host('zhangyan')
    for data in filteredData:
        print(data)
    filteredData = journal.get_by_timestamps('Dec 10 10:50:00', 'Dec 10 10:55:00')
    for data in filteredData:
        print(data)

    
