from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)

        # Set window title and other properties if needed
        self.setWindowTitle("Popup Window")
        self.setGeometry(100, 100, 800, 600)

        # Logo
        self.logoLabel = QLabel(self)
        self.logoPixmap = QPixmap('assets/images/webby.png')  # Replace with your logo path
        scaledPixmap = self.logoPixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logoLabel.setPixmap(scaledPixmap)
        self.logoLabel.setFixedSize(scaledPixmap.size())  # Adjust size based on the scaled image

        # Program Name with larger font
        self.programNameLabel = QLabel("Webby", self)
        font = QFont()
        font.setPointSize(30)  # Set the font size to be 3 times larger
        self.programNameLabel.setFont(font)

        # Paragraph of Text
        self.paragraphLabel = QLabel("Webby checks if your websites are online. It is well suited for many sites in a vertical display format. ", self)
        self.paragraphLabel.setWordWrap(True)

        # Paragraph of Text
        self.paragraphLabel4 = QLabel("Import CSV: no headers. Just a csv with URL, friendly name, and string you want to check for on the site.", self)
        self.paragraphLabel4.setWordWrap(True)

        # Paragraph of Text
        self.paragraphLabel2 = QLabel("This program is released under GNU license.", self)
        self.paragraphLabel2.setWordWrap(True)

        # Paragraph of Text
        self.paragraphLabel3 = QLabel("Coded by ddxfish. https://github.com/ddxfish", self)
        self.paragraphLabel3.setWordWrap(True)

        # OK Button
        self.okButton = QPushButton("OK", self)
        self.okButton.clicked.connect(self.accept)

        # Layouts
        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.logoLabel)
        self.topLayout.addWidget(self.programNameLabel, alignment=Qt.AlignLeft)
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.paragraphLabel)
        self.mainLayout.addWidget(self.paragraphLabel2)
        self.mainLayout.addWidget(self.paragraphLabel3)
        self.mainLayout.addWidget(self.paragraphLabel4)
        self.mainLayout.addWidget(self.okButton, alignment=Qt.AlignCenter)
