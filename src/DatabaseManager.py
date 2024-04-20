import sqlite3
import os
import time
import csv
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow

class DatabaseManager:
    def __init__(self, db_file='website-data.sql'):
        self.db_file = db_file
        db_exists = os.path.exists(db_file)
        self.conn = sqlite3.connect(self.db_file)
        if not db_exists:
            self.init_db()
        self.username = self.get_setting("username")
        self.password = self.get_setting("password")

    def init_db(self):
        """ Initialize the database and create the tables. """
        cursor = self.conn.cursor()
        
        # Create the 'sites' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sites (
                siteID INTEGER PRIMARY KEY AUTOINCREMENT,
                URL TEXT UNIQUE NOT NULL,
                friendlyName TEXT,
                checkString TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                settingID INTEGER PRIMARY KEY AUTOINCREMENT,
                settingName TEXT UNIQUE NOT NULL,
                settingValue TEXT
            )
        ''')
        # Insert default values for 'updateInterval' and 'guiUpdateInterval'
        # This uses 'INSERT OR IGNORE' to avoid inserting duplicates if the entries already exist
        cursor.executemany('''
            INSERT OR IGNORE INTO settings (settingName, settingValue)
            VALUES (?, ?)
        ''', [
            ('startWidth', '1280'),  # Default value for updateInterval, e.g., 600 seconds
            ('startHeight', '1280'), 
            ('updateInterval', '60'), 
            ('guiUpdateInterval', '1')  # Default value for guiUpdateInterval, e.g., 60 seconds
        ])
        # Create the 'website_status' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS website_status (
                statusID INTEGER PRIMARY KEY AUTOINCREMENT,
                siteID INTEGER,
                httpStatus INTEGER,
                sslValid BOOLEAN,
                dnsValid BOOLEAN,
                stringFound BOOLEAN,
                success BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (siteID) REFERENCES sites(siteID)
            )
        ''')
        self.conn.commit()

        cursor.execute('''
            INSERT INTO sites (URL, friendlyName, checkString) 
            VALUES (?, ?, ?)
        ''', ('http://example.com', 'Example Site', 'example'))
        self.conn.commit()
        cursor.execute('''
            INSERT INTO sites (URL, friendlyName, checkString) 
            VALUES (?, ?, ?)
        ''', ('https://yahoo.com', 'Yahoo', 'yahoo'))
        self.conn.commit()
        cursor.execute('''
            INSERT INTO sites (URL, friendlyName, checkString) 
            VALUES (?, ?, ?)
        ''', ('https://ask.com', 'Ask', 'should not be there'))
        self.conn.commit()

    def add_website(self, name, url, checkString):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO sites (friendlyName, URL, checkString) 
            VALUES (?, ?, ?)
        ''', (name, url, checkString))
        self.conn.commit()

    def get_setting(self, setting_name):
        cursor = self.conn.cursor()
        # First, try to get the setting
        cursor.execute('''
            SELECT settingValue FROM settings WHERE settingName = ?
        ''', (setting_name,))
        row = cursor.fetchone()
        # Check if the setting was found
        if row is not None:
            return row[0]
        else:
            # If not found, use add_setting to create a new setting with an empty value
            self.add_setting(setting_name, "")
            # Return the empty value
            return ""

    def set_setting(self, setting_name, value):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO settings (settingName, settingValue)
            VALUES (?, ?)
            ON CONFLICT(settingName) 
            DO UPDATE SET settingValue = excluded.settingValue
        ''', (setting_name, value))
        self.conn.commit()
        
    def add_setting(self, setting_name, value):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO settings (settingName, settingValue)
            VALUES (?, ?)
        ''', (setting_name, value))
        self.conn.commit()

    def remove_website(self, url):
        cursor = self.conn.cursor()
        siteID = self.get_site_id(url)
        # Delete all status data associated with the siteID
        cursor.execute('DELETE FROM website_status WHERE siteID = ?', (siteID,))
        # Delete the site from the sites table
        cursor.execute('DELETE FROM sites WHERE siteID = ?', (siteID,))
        self.conn.commit()

    def get_latest_timestamp_by_status(self, url, success=1):
        """ Get the latest timestamp for a given URL and success/failure status. """
        cursor = self.conn.cursor()
        siteID = self.get_site_id(url)
        # Get the latest timestamp for the given siteID and success/failure status
        cursor.execute('''
            SELECT MAX(timestamp) FROM website_status
            WHERE siteID = ? AND success = ?
        ''', (siteID, success))
        timestamp_result = cursor.fetchone()
        if timestamp_result and timestamp_result[0]:
            return timestamp_result[0]  # Return the latest timestamp
        else:
            return None  # No matching record found

    def get_all_sites(self):
        """ Retrieve all sites from the database. """
        cursor = self.conn.cursor()
        cursor.execute('SELECT URL, friendlyName, checkString FROM sites')
        return cursor.fetchall()
    
    def get_site_id(self, url):
        """ Get the siteID for a given URL from the database. """
        cursor = self.conn.cursor()
        cursor.execute('SELECT siteID FROM sites WHERE URL = ?', (url,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the siteID
        else:
            return None  # URL not found in the database

    #input URL, output URL, name and checkstring
    def get_site_info(self, url):
        cursor = self.conn.cursor()
        # SQL query to select the site information
        query = "SELECT URL, checkString, friendlyName FROM sites WHERE URL = ?"
        try:
            # Execute the query
            cursor.execute(query, (url,))
            result = cursor.fetchone()  # Fetches the first row of the query result
            if result:
                return list(result)  # Convert the result tuple to a list
            else:
                return None  # Return None if no result is found
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def insert_website_status(self, url, http_status, ssl_valid, dnsValid, stringFound, success):
        """ Insert a new website status record into the database with a Unix timestamp. """
        timestamp = int(time.time())  # Get current Unix timestamp
        cursor = self.conn.cursor()
        siteID = self.get_site_id(url)
        cursor.execute('''
            INSERT INTO website_status (siteID, httpStatus, sslValid, dnsValid, stringFound, success, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (siteID, http_status, ssl_valid, dnsValid, stringFound, success, timestamp))
        self.conn.commit()


    def __del__(self):
        """ Close the database connection when the object is destroyed. """
        if self.conn:
            self.conn.close()

    def importCSV(self, parent=None):
        # Open file dialog to select the CSV file
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(parent, "Open CSV", "", "CSV Files (*.csv)", options=options)
        if filePath:
            self.importCSVToDatabase(filePath)

    def importCSVToDatabase(self, filePath):
        # Connect to your SQLite database
        #conn = sqlite3.connect('your_database.db')  # Replace with your database path
        cursor = self.conn.cursor()
        # Read CSV file
        with open(filePath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            #next(reader, None)  # Skip the header row if your CSV has one
            for row in reader:
                try:
                    # Assuming CSV format: URL, friendlyName, checkString
                    cursor.execute("INSERT INTO sites (URL, friendlyName, checkString) VALUES (?, ?, ?)", 
                                   (row[0], row[1], row[2]))
                except sqlite3.IntegrityError:
                    print(f"Duplicate or invalid data for URL: {row[0]}")
        # Commit changes and close the connection
        self.conn.commit()
