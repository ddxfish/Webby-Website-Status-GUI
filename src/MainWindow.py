from PyQt5.QtWidgets import QTableView, QStyledItemDelegate, QAction, QHeaderView, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTableWidget, QTextEdit, QHBoxLayout, QStatusBar, QDialog
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtWidgets import QMainWindow
from src.AddWebsiteDialog import AddWebsiteDialog
from src.RemoveWebsiteDialog import RemoveWebsiteDialog
import datetime
from src.MainAboutWindow import AboutWindow
from src.ImageAndTextDelegate import ImageAndTextDelegate
from src.MainSettingsWindow import SettingsDialog
#from settings import checkInterval, startWidth, startHeight

class MainWindow(QMainWindow):
    def __init__(self, websiteListModel, databaseManager, websiteChecker, TimingManager, parent=None):
        super(MainWindow, self).__init__(parent)
        self.websiteListModel = websiteListModel
        self.databaseManager = databaseManager
        self.websiteChecker = websiteChecker
        self.TimingManager = TimingManager
        self.logoLabel = QLabel(self)
        self.initUI()
        #self.loadSampleData()
    
    def initUI(self):
        # Main Window setup
        self.setWindowTitle('Webby Website Uptime Checker')
        self.setGeometry(100, 100, int(self.databaseManager.get_setting("startWidth")), int(self.databaseManager.get_setting("startHeight")))

        # Menu Bar
        menuBar = self.menuBar()
        # File menu with sub-options
        fileMenu = menuBar.addMenu('File')
        # Add Site action
        addSiteAction = QAction('Add Site', self)
        addSiteAction.triggered.connect(self.addWebsite)
        fileMenu.addAction(addSiteAction)
        # Remove Site action
        removeSiteAction = QAction('Remove Site', self)
        removeSiteAction.triggered.connect(self.removeWebsite)
        fileMenu.addAction(removeSiteAction)
        # Refresh Site action
        refreshSiteAction = QAction('Refresh Site', self)
        refreshSiteAction.triggered.connect(self.refreshStatus)
        fileMenu.addAction(refreshSiteAction)
        # Add Site action
        importSiteAction = QAction('Import CSV (url, name, string)', self)
        importSiteAction.triggered.connect(self.importCSV)
        fileMenu.addAction(importSiteAction)
        # Settings menu with sub-options
        settingsMenu = menuBar.addMenu('Settings')
        # Settings action
        
        settingsAction = QAction('Settings', self)
        settingsAction.triggered.connect(lambda: self.openSettingsDialog(self.databaseManager))
        #settingsAction.triggered.connect(self.open_settings)
        settingsMenu.addAction(settingsAction)

        # About menu (assuming it's just a static menu for now)
        aboutMenu = menuBar.addMenu('About')
        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.callAboutWindow)
        aboutMenu.addAction(aboutAction)

        # aboutMenu.triggered.connect(self.callAboutWindow)
        # fileMenu.addAction(aboutMenu)

        # Logo and Buttons Section
        logoLayout = QHBoxLayout()
        logoLabel = QLabel(self)
        pixmap = QPixmap('assets/images/webby.png')  # Replace with your logo path
        scaled_pixmap = pixmap.scaledToWidth(int(self.width() * 0.08), Qt.SmoothTransformation)
        logoLabel.setPixmap(scaled_pixmap)
        logoLayout.addWidget(logoLabel)

        # Program Name with larger font
        self.programNameLabel = QLabel("Webby", self)
        font = QFont()
        font.setPointSize(30)  # Set the font size to be 3 times larger
        self.programNameLabel.setFont(font)
        logoLayout.addWidget(self.programNameLabel, alignment=Qt.AlignLeft)

        # Reduce spacing and set margins
        logoLayout.setSpacing(10)  # Adjust the spacing value as needed
        logoLayout.setContentsMargins(0, 0, 0, 0)  # Left, Top, Right, Bottom margins
        # Add stretch to push everything to the left
        logoLayout.addStretch()


        # Create a QFont object with a larger size
        buttonFont = QFont()
        buttonFont.setPointSize(13)  # Set the font size to 12 points, adjust as needed

        # 3 horizontal buttons
        buttonLayout = QHBoxLayout()
        addButton = QPushButton('Add')
        addButton.setFont(buttonFont)  # Set the font for addButton
        addButton.clicked.connect(self.addWebsite)

        removeButton = QPushButton('Remove')
        removeButton.setFont(buttonFont)  # Set the font for removeButton
        removeButton.clicked.connect(self.removeWebsite)

        refreshButton = QPushButton('Refresh')
        refreshButton.setFont(buttonFont)  # Set the font for refreshButton
        refreshButton.clicked.connect(self.refreshStatus)

        settingsButton = QPushButton('Settings')
        settingsButton.setFont(buttonFont)  # Set the font for settingsButton
        settingsButton.clicked.connect(self.openSettingsDialog)

        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(removeButton)
        buttonLayout.addWidget(refreshButton)
        buttonLayout.addWidget(settingsButton)

        logoLayout.addLayout(buttonLayout)

        # Setup the table view in the main window to use websiteListModel
        self.tableView = QTableView(self) #This will auto-trigger some calls
        self.tableView.setModel(self.websiteListModel)

        self.tableView.verticalHeader().setVisible(False)

        self.tableView.setItemDelegateForColumn(0, ImageAndTextDelegate(self.tableView))
        # Set the custom delegate for the table
        self.tableView.setItemDelegate(NoEllipsisDelegate(self.tableView))

        # Set stretch or resize mode
        self.header = self.tableView.horizontalHeader()
        self.adjustTableColumnWidths() #set table view columns



        # Main Layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(logoLayout)
        mainLayout.addWidget(self.tableView)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(mainLayout)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        # Log Entry Label (new)
        self.logEntryLabel = QLabel()
        self.logEntryLabel.setText("Current Log Entry: ...")  # Set initial text
        self.statusBar.addWidget(self.logEntryLabel)  # Left aligned by default
        # Time Label
        self.timeLabel = QLabel()
        self.statusBar.addPermanentWidget(self.timeLabel)
        # Update time every minute (the clock)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(20000)  # 60000 milliseconds = 1 minute
        # Green Circle
        # Initialize green circle label
        self.greenCircleLabel = QLabel()
        self.statusBar.addPermanentWidget(self.greenCircleLabel)
        self.changeCircleColor(int(85))  # Default to green
        # Interval Label
        self.intervalLabel = QLabel()
        self.logEntryLabel.setText(str(self.databaseManager.get_setting("updateInterval"))) 
        self.statusBar.addPermanentWidget(self.intervalLabel)
        #self.statusBar.addWidget(self.intervalLabel)  # Left aligned by default
        #Leave this at the end
        self.updateTime()
    
    # def loadSampleData(self):
    #     #['Status', 'Name', 'URL', 'Last Fail', 'Last Seen']
    #     sampleData = [
    #         (200, "http://example.com", "http://example.com", "26m", "28m"),
    #         (303, "http://testsite.com", "http://testsite.com", "1h 55m", "6h 55m")
    #     ]
    #     self.websiteListModel.updateData(sampleData)
    
    #This is for the staus bar circle color
    def changeCircleColor(self, hue): 
        """
        Changes the color of the circle based on hue.
        Hue values for reference:
        - Red: 0
        - Yellow: 43 (~85 * 60 / 255)
        - Green: 85 (~170 * 60 / 255)
        - Violet: 170 (~255 * 60 / 255)
        """
        hue_mapped = hue * 360 / 255  # Map from 0-255 to 0-360
        color = QColor.fromHsv(int(hue_mapped), 255, 255)  # Full saturation and value
        # Create colored pixmap
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(color)
        painter.drawEllipse(0, 0, 16, 16)
        painter.end()
        # Update the pixmap of the label
        self.greenCircleLabel.setPixmap(pixmap)

    def importCSV(self):
        self.databaseManager.importCSV(self)
        self.websiteChecker.load_websites_from_db(1)
        self.websiteChecker.checkAllWebsites()

    def updateLogEntry(self, log_entry):
        # Update log entry label here
        self.logEntryLabel.setText(f"{log_entry}")


    def updateCheckInterval(self, interval=3600):
        # Update log entry label here
        remaining = self.websiteChecker.remainingTime
        remaining = str(int(remaining / 60)) + "m"
        interval = str(float(self.databaseManager.get_setting("updateInterval"))) + "m"
        self.intervalLabel.setText(f"Next: {remaining} / {interval}")

    def updateTime(self):
        self.updateCheckInterval(int(float(self.databaseManager.get_setting("updateInterval")) / 1000))
        self.updateLogEntry(self.websiteChecker.logEntryLabelBuffer)
        self.changeCircleColor(self.websiteChecker.statusCircleColorBuffer)
        currentTime = QDateTime.currentDateTime().toString("HH:mm")
        self.timeLabel.setText(currentTime)
            
    def showEvent(self, event):  #when we show things, resize column width
        super().showEvent(event)
        self.adjustTableColumnWidths()
        self.updateLogoSize()

    def resizeEvent(self, event): #during reize, resize column widths
        super().resizeEvent(event)
        self.adjustTableColumnWidths()
        self.updateLogoSize()

    def addWebsite(self):
        print("trying to open add website dialog")
        dialog = AddWebsiteDialog(self.databaseManager, self.websiteChecker)
        if dialog.exec_():
            print("Website added.")
            self.websiteChecker.checkAllWebsites()
            # Optionally refresh your website list here

    def removeWebsite(self):
        dialog = RemoveWebsiteDialog(self.databaseManager, self.websiteChecker)
        if dialog.exec_():
            print("Website removed.")
            self.websiteChecker.checkAllWebsites()
            # Optionally refresh your website list here

    def openSettingsDialog(self):
        # Create and configure the settings dialog
        settingsDialog = SettingsDialog(self.databaseManager)
        print("trying to open settings")
        #settingsDialog = self.SettingsDialog()
        # Show the dialog and handle the result
        if settingsDialog.exec_() == QDialog.Accepted:
            username = self.databaseManager.get_setting("username")
            password = self.databaseManager.get_setting("password")

    def updateLogoSize(self):
        pixmap = QPixmap('assets/images/webby.png')
        scaled_width = int(self.width() * 0.08)  # Convert to integer
        scaled_pixmap = pixmap.scaledToWidth(scaled_width, Qt.SmoothTransformation)
        self.logoLabel.setPixmap(scaled_pixmap)

    def adjustTableColumnWidths(self):
        tablewidth = self.tableView.width()
        self.header.setSectionResizeMode(0, QHeaderView.Fixed)  # Resize first column to its contents
        self.header.setSectionResizeMode(1, QHeaderView.Fixed)  # Fixed width for second column
        self.header.setSectionResizeMode(2, QHeaderView.Fixed)  # Fixed width for second column
        self.header.setSectionResizeMode(3, QHeaderView.Fixed)  # Fixed width for second column
        self.header.setSectionResizeMode(4, QHeaderView.Stretch)  # Fixed width for second column
        self.tableView.setColumnWidth(0, int(tablewidth * 0.1))  # Set width for the fixed-width column
        self.tableView.setColumnWidth(1, int(tablewidth * 0.25))  # Set width for the fixed-width column
        self.tableView.setColumnWidth(2, int(tablewidth * 0.45))  # Set width for the fixed-width column
        self.tableView.setColumnWidth(3, int(tablewidth * 0.1))  # Set width for the fixed-width column
        #self.tableView.setColumnWidth(4, tablewidth * 0.2)  # Set width for the fixed-width column

    def callAboutWindow(self):
        # Create and display the popup
        popup = AboutWindow()
        popup.exec_()

    def refreshStatus(self):
        self.updateLogEntry(self.websiteChecker.logEntryLabelBuffer)
        self.websiteChecker.checkAllWebsites()
        self.TimingManager.restartTimer2()

    def openSettings(self):
        pass

class NoEllipsisDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.textElideMode = Qt.ElideNone  # Prevent text ellipsis
        super().paint(painter, option, index)