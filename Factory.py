import abc
from LogEntries import *

class Factory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_sshLog(self, raw_log):
        pass

class Factory_Failed_Pass(Factory):
    def create_sshLog(self, raw_log):
        return SSHLogEntryFailedPass(raw_log)
    
class Factory_Accepted_Pass(Factory):
    def create_sshLog(self, raw_log):
        return SSHLogEntryAcceptedPass(raw_log)
    
class Factory_Error(Factory):
    def create_sshLog(self, raw_log):
        return SSHLogEntryError(raw_log)

class Factory_Other(Factory):
    def create_sshLog(self, raw_log):
        return SSHLogOther(raw_log)