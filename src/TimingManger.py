from PyQt5.QtCore import QTimer
#from settings import checkInterval, guiInterval

class TimingManager:
    def __init__(self, websiteChecker, databaseManager):
        self.websiteChecker = websiteChecker
        self.databaseManager = databaseManager

        # Interval for checking websites (in milliseconds)
        self.checkInterval = 60000 * float(self.databaseManager.get_setting("updateInterval"))  # 60 seconds * minutes
        self.guiInterval = 60000 * float(self.databaseManager.get_setting("guiUpdateInterval"))

        # Immediately check all websites once upon initialization
        self.checkAllWebsites()

        # Timer to trigger website checks
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkAllWebsites)
        self.timer.start(int(self.checkInterval))

        # Timer to trigger gui update
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.updateGui)
        self.timer2.start(int(self.guiInterval))

        #Get other stuff like interval updated to gui
        self.updateGui()

    def restartTimer2(self):
        self.timer2.start(int(self.guiInterval))

    def getTimeUntilCheck(self):
        # Get the remaining time in milliseconds and convert to seconds
        remainingTimeMs = self.timer.remainingTime()
        if remainingTimeMs < 0:  # If the timer is not active, remainingTime() returns -1
            return 0
        return int(remainingTimeMs / 1000)  # Convert milliseconds to seconds
    
    def updateGui(self):
        print("Timing Manager: update gui")
        self.websiteChecker.refreshMainTable(self.getTimeUntilCheck())

    def checkAllWebsites(self):
        print("Timing Manager: Checking all sites")
        self.websiteChecker.checkAllWebsites()

        # Example: You might iterate over a list of websites and check each one
        # for website in self.websites:
        #     self.checkWebsite(website)
        
