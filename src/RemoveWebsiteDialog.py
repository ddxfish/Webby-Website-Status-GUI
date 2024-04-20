from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QVBoxLayout, QPushButton
from src.Website import Website


class RemoveWebsiteDialog(QDialog):
    def __init__(self, databaseManager, websiteChecker, parent=None):
        super().__init__(parent)
        self.websiteChecker = websiteChecker
        self.databaseManager = databaseManager
        self.initUI()

    def initUI(self):
        # Main Window setup
        self.setWindowTitle('Website Uptime Settings')
        self.setGeometry(100, 100, 800, 600)
        
        self.setWindowTitle("Remove Website")
        self.layout = QVBoxLayout(self)

        # URL Input
        self.urlLabel = QLabel("URL of the Website to Remove:")
        self.urlEdit = QLineEdit(self)
        self.layout.addWidget(self.urlLabel)
        self.layout.addWidget(self.urlEdit)

        # Remove Button
        self.removeButton = QPushButton("Remove Website", self)
        self.removeButton.clicked.connect(self.removeWebsite)
        self.layout.addWidget(self.removeButton)

    def removeWebsite(self):
        url = self.urlEdit.text()
        url, name, checkString = self.databaseManager.get_site_info(url)

        # add website to website checker object
        thiswebsite = Website(url, name, checkString)
        self.websiteChecker.removeWebsite(thiswebsite)

        url = self.urlEdit.text()
        self.databaseManager.remove_website(url)
        self.accept()
