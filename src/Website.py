class Website:
    def __init__(self, url, name, checkString=None):
        self.url = url
        self.name = name
        self.checkString = checkString
        self.lastFail = None
        self.lastSeen = None
        self.httpStatus = None
        self.isValidSSL = False
        self.hasValidDNS = False
        self.containsString = False
        self.success = False

    def __str__(self):
        return (f"Website(Name: {self.name}, URL: {self.url}, "
            f"HTTP Status: {self.httpStatus}, SSL Valid: {self.isValidSSL}, "
            f"DNS Valid: {self.hasValidDNS}, Contains String: {self.containsString}, "
            f"Last Seen: {self.lastSeen}, Last Fail: {self.lastFail})")

    def checkStatus(self):
        return True