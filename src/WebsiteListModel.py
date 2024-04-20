from PyQt5.QtCore import QAbstractTableModel, Qt

class WebsiteListModel(QAbstractTableModel):
    def __init__(self, databaseManager):
        super().__init__()
        self.databaseManager = databaseManager
        self.websiteData = []  # Internal storage for the website data

    def rowCount(self, parent=None):
        rowCount = len(self.websiteData)
        #print("Row count:", rowCount)  # Debug print
        return rowCount

    def columnCount(self, parent=None):
        #print("Column count: 5")
        # Returns the number of columns in the model
        return 5  # Adjust based on the number of columns in your data

    def data(self, index, role=Qt.DisplayRole):
        #print("entered data function")
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        data = self.websiteData[index.row()][index.column()]
        #print("Data at [", index.row(), ",", index.column(), "]:", data)  # Debug print
        return data

    def headerData(self, section, orientation, role):
        #print("headerdata function:")
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # Provide column headers
            #print("headerData: " + ['Status', 'Name', 'URL', 'Last Fail', 'Last Seen'][section])
            return ['Status', 'Name', 'URL', 'Last Fail', 'Last Seen'][section]
        return None

    def updateData(self, newData, remaining=0):
        # Update the model with new data
        self.beginResetModel()
        self.websiteData = newData
        print("updateData:")
        #print(self.websiteData)
        self.endResetModel()  # Notify the view to update itself
