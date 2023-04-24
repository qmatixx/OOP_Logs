from Factory import *
from Utils import get_message_type
from datetime import datetime
import ipaddress
import re

class SSHLogJournal:

    def __init__(self, logList = []):
        self.logList = logList

    def __len__(self): return len(self.logList)

    def __iter__(self): return iter(self.logList)

    def __contains__(self, log):
        return log in self.logList
    
    def append(self, raw_log):
        sshEntry = Factory_Manager.create_log(raw_log)
        if sshEntry.validate():
            self.logList.append(sshEntry)
            return True
        return False

    # def get_creator(self, raw_log: str) -> Factory:
    #     type = get_message_type(raw_log)
    #     if type == "Authentication succeeded.":
    #         return Factory_Accepted_Pass()
    #     elif type == "Incorrect password.":
    #         return Factory_Failed_Pass()
    #     elif type == "Error.":
    #         return Factory_Error()
    #     else:
    #         return Factory_Other()
        
    def get_by_host(self, key_host=None):
        return [entry for entry in self.logList if entry.host == key_host]

    def get_by_timestamps(self, timestamp1, timestamp2):
        innerList = []
        for entry in self.logList:
            date_low = datetime.strptime(timestamp1,"%b %d %H:%M:%S")
            date_high = datetime.strptime(timestamp2,"%b %d %H:%M:%S")
            if entry.timestamp >= date_low and entry.timestamp <= date_high:
                innerList.append(entry)
        return innerList
    
    def __getattr__(self, attr):
        if attr.startswith('ip_'):
            ip = attr[3:].replace("_", ".")
            ipv4 = ipaddress.IPv4Address(ip)
            return [entry for entry in self.logList if entry.get_ipv4()==ipv4]
        # elif attr.startswith('index_'):
        #     index = attr[6:]
        #     if '_' in index:
        #         indexList = index.split("_")
        #         try:
        #             if len(indexList)==2:
        #                 return self[int(indexList[0]):int(indexList[1])]
        #             if len(indexList)==3:
        #                 return self[int(indexList[0]):int(indexList[1]):int(indexList[2])]
        #             else:
        #                 raise ValueError("Invalid index value")
        #         except ValueError:
        #             print("Invalid index value")
        elif attr.startswith('index_'):
            pid = int(attr[6:])
            return [entry for entry in self.logList if entry.pid==pid]
        elif attr.startswith('date_'):
            date_pattern = r'(.+)\s(\d+)'
            dateStr = attr[5:].replace("_"," ")
            match = re.search(date_pattern, dateStr)
            if match:
                date = datetime.strptime(dateStr,"%b %d")
                return [entry for entry in self.logList if entry.timestamp.month == date.month and entry.timestamp.day == date.day]
        else:
            raise AttributeError(f"'SSH Journal' has no attribute '{attr}'")
        
    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self.logList))
            return [self.logList[ii] for ii in range(start,stop,step)]
        elif isinstance(key, int):
            return self.logList[key]
        raise ValueError("Invalid index provided")

        

if __name__ == "__main__":
    journal = SSHLogJournal()
    with open("logs.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            journal.append(line)
    for log in journal:
        print(log.get_ipv4())
    # filteredData = journal.get_by_host('zhangyan')
    # for data in filteredData:
    #     print(data)
    filteredData = journal.get_by_timestamps('Dec 10 7:00:00', 'Dec 10 23:55:00')
    for data in filteredData:
        print(data)
    # filteredData = journal.ip_103_99_0_122
    # for data in filteredData:
    #     print(data)
    # filteredData = journal[1:100:5]
    # for data in filteredData:
    #     print(data)
    # filteredData = journal.date_Dec_10
    # for data in filteredData:
    #     print(data)
    # filteredData = journal.index_24563
    # for data in filteredData:
    #     print(data)
    

    
