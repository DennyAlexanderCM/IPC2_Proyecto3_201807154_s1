class Company():
    def __init__(self):
        self.name = None
        self.service = None
    
    def setName(self, name):
        self.name = name
    
    def setService(self, service):
        self.service = service

    def getName(self):
        return self.name
    
    def getService(self):
        return self.service