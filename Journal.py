
class SSHLogJournal:

    def __init__(self, logList = []):
        self.logList = logList

    def __len__(self): return len(self.logList)

    def __iter__(self): return iter(self.logList)

    def __contains__(self, log):
        return log in self.logList
    
    