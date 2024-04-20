from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
import sys
class SettingsDialog(QDialog):
    def __init__(self, databaseManager, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.databaseManager = databaseManager
        self.settings = {
            'update_interval': self.databaseManager.get_setting('updateInterval'),
            'gui_update_interval': self.databaseManager.get_setting('guiUpdateInterval'),
            'start_width': self.databaseManager.get_setting('startWidth'),
            'start_height': self.databaseManager.get_setting('startHeight')
        }
        self.initUI()

    def get_setting(self, setting_name):
        return self.databaseManager.get_setting(setting_name)

    def add_setting(self, setting_name, value):
        self.databaseManager.add_setting(setting_name, value)

    def initUI(self):
        # Main Window setup
        self.setWindowTitle('Website Uptime Settings')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        # Form layout for settings
        self.formLayout = QFormLayout()
        self.layout.addLayout(self.formLayout)

        # Update Interval Field
        self.updateIntervalLineEdit = QLineEdit(self)
        self.updateIntervalLineEdit.setText(self.settings['update_interval'])
        self.formLayout.addRow(QLabel("Update Interval:"), self.updateIntervalLineEdit)

        # GUI Update Interval Field
        self.guiUpdateIntervalLineEdit = QLineEdit(self)
        self.guiUpdateIntervalLineEdit.setText(self.settings['gui_update_interval'])
        self.formLayout.addRow(QLabel("GUI Update Interval:"), self.guiUpdateIntervalLineEdit)

        # Start Width Field
        self.startWidthLineEdit = QLineEdit(self)
        # Start Height Field
        self.startHeightLineEdit = QLineEdit(self)
        
        # Attempt to fetch the size of the main window if parent is set
        if self.parent():
            self.startWidthLineEdit.setText(str(self.parent().width()))
            self.startHeightLineEdit.setText(str(self.parent().height()))
        else:
            # Use database values if no parent window is available
            self.startWidthLineEdit.setText(self.settings['start_width'])
            self.startHeightLineEdit.setText(self.settings['start_height'])

        self.formLayout.addRow(QLabel("Start Width:"), self.startWidthLineEdit)
        self.formLayout.addRow(QLabel("Start Height:"), self.startHeightLineEdit)

        # OK and Cancel buttons
        self.buttonsLayout = QHBoxLayout()
        self.okButton = QPushButton("OK", self)
        self.okButton.clicked.connect(self.saveSettings)
        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.clicked.connect(self.reject)
        self.buttonsLayout.addWidget(self.okButton)
        self.buttonsLayout.addWidget(self.cancelButton)
        self.layout.addLayout(self.buttonsLayout)

    def saveSettings(self):
        # Get current values from line edits
        update_interval = self.updateIntervalLineEdit.text()
        gui_update_interval = self.guiUpdateIntervalLineEdit.text()
        start_width = self.startWidthLineEdit.text()
        start_height = self.startHeightLineEdit.text()

        # Save new settings to the database
        self.databaseManager.set_setting('updateInterval', update_interval)
        self.databaseManager.set_setting('guiUpdateInterval', gui_update_interval)
        self.databaseManager.set_setting('startWidth', start_width)
        self.databaseManager.set_setting('startHeight', start_height)

        # Close the dialog
        self.accept()

        sys.exit(42)
