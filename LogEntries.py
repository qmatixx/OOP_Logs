# First task
import re, sys
import ipaddress
from ipaddress import AddressValueError
from parse_log import parse_ssh_log
from Utils import *
import abc

# Class that represents a single log
class SSHLogEntry(metaclass=abc.ABCMeta):
    # Constructor for a log represented by a raw log
    @abc.abstractmethod
    def __init__(self, log):
        log_dict = parse_ssh_log(log)
        self.timestamp = log_dict['timestamp']
        self.host = get_user_from_log(log_dict['message'])
        self.process_name = log_dict['process_name']
        self.pid = log_dict['pid']
        self.message = log_dict['message']
        self._raw_log = log
    
    # To string method
    def __str__(self):
        user = self.host
        if self.host is None or self.host=='unknown':
            user = "Uknown user"
        return f"{user} - {self.timestamp} {self.process_name}[{self.pid}]: {self.message}"

    def get_ipv4(self):
        ipv4_list = get_ipv4s_from_log(self.message)
        if not ipv4_list:
            return None
        else:
            try:
                return ipaddress.IPv4Address(ipv4_list[0])
            except AddressValueError:
                return None
    
    @abc.abstractmethod
    def validate(self):
        print("Validating log: ", self.message)

    @property
    def has_ip(self):
        return self.get_ipv4() is not None
    
    def __repr__(self):
        reprString = f'SSHLogEntry({self.timestamp},{self.process_name},[{self.pid}],{self.message})'
        return reprString

    def __eq__(self, other):
        return self.timestamp == other.timestamp and self.message == other.message

    def __lt__(self, other):
        return (self.timestamp, self.message) < (other.timestamp, other.message)

    def __gt__(self, other):
        return (self.timestamp, self.message) > (other.timestamp, other.message)
        
class SSHLogEntryFailedPass(SSHLogEntry):

    def __init__(self, log):
        super().__init__(log)
        attributes = failedPasswordArgs(self.message)
        if not(attributes==None):
            self.address = attributes[0]
            self.port = attributes[1]

    def validate(self):
        super().validate()
        log_dict = parse_ssh_log(self._raw_log)
        attributes = failedPasswordArgs(log_dict['message'])
        if attributes == None: return False
        return (self.timestamp == log_dict['timestamp']
                and self.host == get_user_from_log(log_dict['message'])
                and self.process_name == log_dict['process_name']
                and self.pid == log_dict['pid']
                and self.message == log_dict['message']
                and self.address == attributes[0]
                and self.port == attributes[1])

class SSHLogEntryAcceptedPass(SSHLogEntry):

    def __init__(self, log):
        super().__init__(log)
        attributes = acceptedPasswordArgs(self.message)
        if not(attributes==None):
            self.address = attributes[0]
            self.port = attributes[1]

    def validate(self):
        super().validate()
        log_dict = parse_ssh_log(self._raw_log)
        attributes = failedPasswordArgs(log_dict['message'])
        if attributes == None: return False
        return (self.timestamp == log_dict['timestamp']
                and self.host == get_user_from_log(log_dict['message'])
                and self.process_name == log_dict['process_name']
                and self.pid == log_dict['pid']
                and self.message == log_dict['message']
                and self.address == attributes[0]
                and self.port == attributes[1])

class SSHLogEntryError(SSHLogEntry):

    def __init__(self, log):
        super().__init__(log)
        attributes = acceptedPasswordArgs(self.message)
        if not(attributes==None):
            self.address = attributes[0]
            self.errNumber = attributes[1]
            self.errMessage = attributes[2]

    def validate(self):
        super().validate()
        log_dict = parse_ssh_log(self._raw_log)
        attributes = errorArgs(log_dict['message'])
        if attributes == None: return False
        return (self.timestamp == log_dict['timestamp']
                and self.host == get_user_from_log(log_dict['message'])
                and self.process_name == log_dict['process_name']
                and self.pid == log_dict['pid']
                and self.message == log_dict['message']
                and self.address == attributes[0]
                and self.errNumber == attributes[1]
                and self.errMessage == attributes[2])
    
class SSHLogOther(SSHLogEntry):

    def __init__(self, log):
        super().__init__(log)

    def validate(self):
        super().validate()
        return True
    

if __name__ == '__main__':
    with open("logs.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            log = parse_ssh_log(line)
            sshLogEntry_dict = SSHLogEntry(log)
            print(sshLogEntry_dict)
            print(sshLogEntry_dict.get_ipv4())
            print()