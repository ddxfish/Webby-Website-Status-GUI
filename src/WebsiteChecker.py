import requests
import datetime
import re
import dns.resolver
from types import SimpleNamespace
from src.Website import Website

class WebsiteChecker:
    def __init__(self, databaseManager, websiteListModel, checkInterval=30, data_updated_callback=None):
        self.websites = []
        self.checkInterval = checkInterval
        self.databaseManager = databaseManager
        self.websiteListModel = websiteListModel
        self.remainingTime = -1
        self.logEntryLabelBuffer = ""
        #self.checkAllWebsites()
        self.statusCircleColorBuffer = 255
        self.load_websites_from_db()

    def addWebsite(self, website):
        self.websites.append(website)

    def removeWebsite(self, website):
        # Find the tuple by matching the URL
        url = website.url
        website_to_remove = None
        for site in self.websites:
            if site.url == url:
                website_to_remove = site
                break
        # If the website is found, remove it from the list
        if website_to_remove:
            self.websites.remove(website_to_remove)
            print(f"Website removed: {website_to_remove}")
        else:
            print(f"Website not found: {url}")

    def load_websites_from_db(self, freshclear=0):
        if freshclear == 1:
            self.websites = []
        """ Load websites from the database and add them to the checker. """
        sites = self.databaseManager.get_all_sites()
        for site in sites:
            url, name, checkString = site
            self.addWebsite(Website(url, name, checkString))

    def checkAllWebsites(self):
        updatedData = []
        self.statusCircleColorBuffer = 85 #status is assumed green to start
        for website in self.websites:
            self.getResponse(website)
            success = False

            
            # after we insert, set image
            if (website.httpStatus == 200 and website.sslValid and website.dnsValid and website.containsString):
                website.success = True
                # Insert data into the database
                self.databaseManager.insert_website_status(website.url, website.httpStatus, website.sslValid, website.dnsValid, website.containsString, website.success)
                website.httpStatus = self.set_http_status(website.httpStatus, 1) 
            else: 
                website.success = False
                # Insert data into the database
                self.databaseManager.insert_website_status(website.url, website.httpStatus, website.sslValid, website.dnsValid, website.containsString, website.success)
                if not website.dnsValid: website.httpStatus = "DNS"
                elif not website.sslValid: website.httpStatus = "SSL"
                elif website.httpStatus is not 200: pass
                elif not website.containsString: website.httpStatus = "STR"
                #format it with the image now
                website.httpStatus = self.set_http_status(website.httpStatus, 0) 
                self.statusCircleColorBuffer = 0 #set 
          
            #Send to the GUI
            website.lastFail = self.time_ago(self.databaseManager.get_latest_timestamp_by_status(website.url, 0))
            website.lastSeen = self.time_ago(self.databaseManager.get_latest_timestamp_by_status(website.url, 1))
                     
            newdata = (website.httpStatus, website.name, website.url, website.lastFail, website.lastSeen)
            updatedData.append(newdata)
            #print(newdata)
        self.websiteListModel.updateData(updatedData)


    def refreshMainTable(self, remaining=0):
        updatedData = []
        # remaining time for gui
        if remaining > 0:
            self.remainingTime = remaining

        #self.statusCircleColorBuffer = 85 #status is assumed green to start
        for website in self.websites:
            #Send to the GUI
            website.lastFail = self.time_ago(self.databaseManager.get_latest_timestamp_by_status(website.url, 0))
            website.lastSeen = self.time_ago(self.databaseManager.get_latest_timestamp_by_status(website.url, 1))
                     
            newdata = (website.httpStatus, website.name, website.url, website.lastFail, website.lastSeen)
            updatedData.append(newdata)
            #print("Refreshing main table:")
            #print(newdata)
        self.websiteListModel.updateData(updatedData, remaining)

    def set_http_status(self, status_code, success):
        if success == 1:
            image_path = f'assets/images/green.png'  # Modify this according to your image path logic
        else:
            image_path = f'assets/images/red.png'  # Modify this according to your image path logic
        return (image_path, status_code)
        #self.statusCircleColorBuffer = 85 ######################

    def getResponse(self, website):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
        try:
            response = requests.get(website.url, headers=headers)
            website.sslValid = False if "http://" in website.url else True
            website.httpStatus = response.status_code
            # Check if the response content and the string to check are not None
            if response.content is not None and website.checkString is not None:
                website.containsString = website.checkString in str(response.content)
            else:
                website.containsString = False
        except requests.exceptions.SSLError:
            print(f"SSL certificate failure for {website.url}, adding pseudo responses")
            self.logEntryLabelBuffer = (f"SSL certificate failure for {website.url}, adding pseudo responses")
            response = SimpleNamespace(status_code=-2, content=-2, elapsed=datetime.timedelta(seconds=0))
            website.sslValid = False
            website.containsString = False
        except Exception as e:
            print(f"Error requesting the site {website.url}: {e}, adding pseudo responses")
            self.logEntryLabelBuffer = (f"Error requesting the site {website.url}: {e}, adding pseudo responses")
            response = SimpleNamespace(status_code=-1, content=-1, elapsed=datetime.timedelta(seconds=0))
            website.sslValid = False
            website.containsString = False

        website.httpStatus = response.status_code
        website.lastSeen = datetime.datetime.now() if website.httpStatus == 200 else None
        website.lastFail = datetime.datetime.now() if website.httpStatus != 200 else None
        website.dnsValid = self.getDnsResponse(str(website.url))

        if website.httpStatus is not 200: 
            self.logEntryLabelBuffer = (f"{str(website.httpStatus)} {website.url}")
        if not website.containsString:
            self.logEntryLabelBuffer = (f"{str(website.containsString)} {website.url}")

        
        print(f"Checked Website URL: {website.url}")
        # print(f"HTTP Status: {website.httpStatus}")
        # print(f"SSL Valid: {website.sslValid}")
        # if website.lastFail:
        #     print(f"Last Fail: {website.lastFail}")
        # if website.lastSeen:
        #     print(f"Last Seen: {website.lastSeen}")
        # print(f"Contains Specified String: {'Yes' if website.containsString else 'No'}")
        # print(f"DNS Valid: {'Present' if website.dnsValid else 'Absent'}")


    def time_ago(self, unix_timestamp):
        # Parse the Unix timestamp
        if unix_timestamp is None:
            return "never"
        if isinstance(unix_timestamp, str):
            unix_timestamp = int(unix_timestamp)
        
        # Convert to a datetime object
        timestamp_datetime = datetime.datetime.fromtimestamp(unix_timestamp)
        
        # Calculate the time difference
        now = datetime.datetime.now()
        diff = now - timestamp_datetime
        
        # Check if the difference is less than 1 minute
        if diff.total_seconds() < 60:
            return "just now"
        
        # Extract days, hours, and minutes
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Format the string conditionally based on days and hours
        time_str = ""
        if days > 0:
            time_str += f"{days}d "
        if hours > 0:
            time_str += f"{hours}h "
        time_str += f"{minutes}m"
        
        return time_str.strip()

    def getDnsResponse(self, query="example.com", nameserver="1.1.1.1", qtype="A"):
        # Remove protocol and path from the URL to get the domain
        domain = re.sub(r'^https?://', '', query)
        domain = re.sub(r'/.*$', '', domain)
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [nameserver]
        try:
            # Perform the DNS resolution
            answer = resolver.resolve(domain, qtype)
            #print(f"DNS resolved for {domain}: {answer[0]}")
            return True
        except Exception as e:
            #print(f"DNS resolution failed for {domain}: {e}")
            return False