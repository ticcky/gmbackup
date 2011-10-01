#!/usr/bin/python
import imaplib
import string, random
import StringIO, rfc822
import os
from datetime import *
import time

# config
BACKUP_DIR = ""
BACKUP_IMAP_FOLDER = "[Gmail]/Todos"
SERVER = "imap.gmail.com"
USER  = ""
PASSWORD = ""

# constants
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
          "Oct", "Nov", "Dec"]
STAT_OK = "OK"
DATETIME_FORMAT = "%Y-%m-%d"

class GMBackup:
    def __init__(self, server, user, password, dst_dir):
        self.server = server
        self.user = user
        self.password = password
        self.dst_dir = dst_dir
        self.conn = None
    
    def connect(self):
        # connect to server
        self.conn = imaplib.IMAP4_SSL(self.server)
        self.conn.login(self.user, self.password)

    def backup(self, from_date = None, to_date = None):
        status, num = self.conn.select(BACKUP_IMAP_FOLDER, True)
	total_cnt = int(num[0])
        if status != STAT_OK:
            return False
        
        day_cntr = 1
        last_day = None

        cfgf = os.path.join(self.dst_dir, "gb.conf")
        try:
            f = open(cfgf, "r")
            last_d = f.read().strip()
            last_d = datetime.strptime(last_d, DATETIME_FORMAT)
            f.close()
        except:
            last_d = None

        if last_d is not None:
            search_d = "%.2d-%s-%.4d" % (last_d.day, MONTHS[last_d.month-1],
                                         last_d.year) #d.strftime("%d-%b-%Y")
        else:
            search_d = None
        
        # list items on server
        if search_d is None:
            search_str = "ALL"
        else:
            search_str = "(SINCE %s)" % search_d

        resp, items = self.conn.search(None, search_str)
        items = string.split(items[0])
	cntr = 0
	
        # fetch items
        for i in items:
	    cntr += 1	    
            # get full message
            resp, data = self.conn.fetch(i, "(RFC822)")            
            text = data[0][1]

            file = StringIO.StringIO(text)
            message = rfc822.Message(file)
            print '* [%d%%] %d/%d fetching' % (int(100 * cntr / len(items)), cntr, len(items),), 
	    try:
	    	print message['date']
	    except:
		pass
            
	    try:
            	t = time.mktime(rfc822.parsedate(message['date']))
            	d = date.fromtimestamp(t)
	    except:
		d = date(1980,1,1)
            if last_day == d:
                day_cntr += 1
            else:
                last_day = d
                day_cntr = 1
            
            # save it
            pth = self.getpath(d)
            if not os.path.exists(pth):
                os.makedirs(pth)
            fpth = os.path.join(pth, str(day_cntr) + ".eml")

            f = open(fpth, "w")
            f.write(text)
            f.close()
            
            # save last processed message timestamp
            f = open(cfgf, "w")
            f.write(d.strftime(DATETIME_FORMAT))
            f.close()

    def getpath(self, d):
        return reduce(os.path.join, [self.dst_dir, str(d.year), str(d.month),
                              str(d.day)])

    def disconnect(self):
        self.conn.logout()

if __name__ == "__main__":
    gmb = GMBackup(SERVER, USER, PASSWORD, dst_dir = BACKUP_DIR)
    gmb.connect()
    done = False
    while not done:
	try:
    		gmb.backup()
	except Exception, e:
		print e
	done = True
    gmb.disconnect()
