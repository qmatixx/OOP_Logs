# First task
import re, sys
from parse_log import parse_ssh_log

# Class that represemnts a single log
class SSHLogEntry:
    # Constructor for a log represented by a dictionary
    def __init__(self, log_dic):
        self.timestamp = log_dic['timestamp']
        self.host = log_dic['host']
        self.process_name = log_dic['process_name']
        self.pid = int(log_dic['pid'])
        self.message = log_dic['message']
        self.log_string = None
    
    # # Constructor for a log represented by a string
    # def __init__(self, log_string):
    #     self.log_string = log_string
    #     self.timestamp = None
    #     self.host = None
    #     self.process_name = None
    #     self.pid = None
    #     self.message = None
    
    # # Method that parses a log represented by a string
    # def parse_log(self):
    #     pattern = r'^(.+)\s(\d+)\s(\d{2}:\d{2}:\d{2})\s(.+)\s(sshd)\[(\d+)\]:\s(.+)$'
    #     match = re.match(pattern, self.log_string)
    #     stringDate = match.group(1) + ' ' + match.group(2) + ' ' + match.group(3)
    #     host = match.group(4)
    #     process_name = match.group(5)
    #     pid = match.group(6)
    #     message = match.group(7)
    #     self.timestamp = stringDate
    #     self.host = host
    #     self.process_name = process_name
    #     self.pid = int(pid)
    #     self.message = message
    
    # To string method
    def __str__(self):
        return f"{self.timestamp} {self.host} {self.process_name}[{self.pid}]: {self.message}"

            
    # Method that returns the IP address from its message and None if there is no IP address
    def get_ipv4(self):
        # Znalazłem taki regex śmieszny w necie, ale nie wiem jak działa XD
        pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        match = re.search(pattern, self.message)
        if match:
            return Ipv4(match.group(0))
        else:
            return None
        
class Ipv4:
    def __init__(self, ip):
        self.ip = ip
        
    def __str__(self):
        return self.ip

if __name__ == '__main__':
    with open("logs.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            log = parse_ssh_log(line)
            sshLogEntry_dict = SSHLogEntry(log)
            print(sshLogEntry_dict)
            print(sshLogEntry_dict.get_ipv4())
            print()