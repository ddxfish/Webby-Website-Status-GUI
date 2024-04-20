import sys
from PyQt5.QtWidgets import QApplication
from src.MainWindow import MainWindow
from src.WebsiteChecker import WebsiteChecker
#from src.Website import Website
from src.WebsiteListModel import WebsiteListModel
from src.DatabaseManager import DatabaseManager
from src.TimingManger import TimingManager
from PyQt5.QtGui import QFont


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.databaseManager = DatabaseManager()
        self.websiteListModel = WebsiteListModel(self.databaseManager)
        self.websiteChecker = WebsiteChecker(self.databaseManager, self.websiteListModel)
        

        # Example: Add websites to the checker
        #self.websiteChecker.addWebsite(Website("https://example.org", "Example", "example"))
        #self.websiteChecker.checkAllWebsites()

        self.TimingManager = TimingManager(self.websiteChecker, self.databaseManager)

        # Initialize the main window
        self.mainWindow = MainWindow(self.websiteListModel, self.databaseManager, self.websiteChecker, self.TimingManager)

        # Display the main window
        self.mainWindow.show()

        

if __name__ == "__main__":
    app = App(sys.argv)
    # Set the default font size # there is no law here
    defaultFont = QFont()
    defaultFont.setPointSize(10)  # Set your desired default font size here
    app.setFont(defaultFont)

    app.setStyleSheet("""
        QWidget {
            background-color: #2b2b2b;
            color: white;
        }
        QHeaderView::section {
            background-color: #333333;
            color: white;
        }
        QTableView QHeaderView::section {
            background-color: #555555;
            color: white;
        }
        QMenuBar::item:selected {  /* When selected */
            background-color: #333333;  /* Darker grey */
        }
        QMenuBar::item:hover {  /* When hovered */
            background-color: #333333;  /* Darker grey */
        }
        QMenu {
            border: 1px solid #111111;  /* Black border for the dropdown */
        }
        QPushButton {
            border: 3px solid #222222; /* 2px outline */
            padding: 15px 30px;
            background-color: #444444;
        }


    """)
    sys.exit(app.exec_())