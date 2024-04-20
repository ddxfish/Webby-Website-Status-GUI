from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QVBoxLayout, QPushButton
from src.Website import Website

class AddWebsiteDialog(QDialog):
    def __init__(self, databaseManager, websiteChecker, parent=None):
        super().__init__(parent)
        self.databaseManager = databaseManager
        self.websiteChecker = websiteChecker
        self.initUI()

    def initUI(self):
        # Main Window setup
        self.setWindowTitle('Website Uptime Settings')
        self.setGeometry(100, 100, 800, 600)
        
        self.setWindowTitle("Add New Website")
        self.layout = QVBoxLayout(self)

        # Friendly Name
        self.nameLabel = QLabel("Friendly Name:")
        self.nameEdit = QLineEdit(self)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.nameEdit)

        # URL
        self.urlLabel = QLabel("URL:")
        self.urlEdit = QLineEdit(self)
        self.layout.addWidget(self.urlLabel)
        self.layout.addWidget(self.urlEdit)

        # Check String
        self.checkStringLabel = QLabel("Check String:")
        self.checkStringEdit = QLineEdit(self)
        self.layout.addWidget(self.checkStringLabel)
        self.layout.addWidget(self.checkStringEdit)

        # Add Button
        self.addButton = QPushButton("Add Website", self)
        self.addButton.clicked.connect(self.addWebsite)
        self.layout.addWidget(self.addButton)

    def addWebsite(self):
        name = self.nameEdit.text()
        url = self.urlEdit.text()
        checkString = self.checkStringEdit.text()

        # add website to website checker object
        thiswebsite = Website(url, name, checkString)
        self.websiteChecker.addWebsite(thiswebsite)

        # Add website to the database
        self.databaseManager.add_website(name, url, checkString)
        self.accept()