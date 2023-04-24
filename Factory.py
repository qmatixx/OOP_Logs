import abc
from LogEntries import *
from Utils import get_message_type

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
    
class Factory_Manager:
    @staticmethod
    def create_log(raw_log):
        creator = Factory_Manager.get_creator(raw_log)
        return creator.create_sshLog(raw_log)

    @staticmethod
    def get_creator(raw_log: str) -> Factory:
        type = get_message_type(raw_log)
        creatorDict = Factory_Manager.get_creator_dict()
        for key, value in creatorDict.items():
            if key == type:
                return value()
        return creatorDict["Other."]()
    
    @staticmethod
    def get_creator_dict():
        types = ["Authentication succeeded.","Incorrect password.","Error.","Other."]
        creators = [Factory_Accepted_Pass, Factory_Failed_Pass, Factory_Error, Factory_Other]
        return dict(zip(types, creators))
