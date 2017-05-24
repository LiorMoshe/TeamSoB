import ftplib
import sys
import os
import time
import random

def downloadFile(ftp, fileName):

    ftp.retrbinary('RETR ' + fileName, open(fileName, 'wb').write, 1024)
	
 
cur = 0
while(True):
  ftp = ftplib.FTP('127.0.0.1') #I hope it works.
  try:
    for j in range(random.randint(0, 15)):
      ftp.login('msfadmin','msfadmin')
      downloadFile(ftp, 'myfile' + str(cur))
      os.remove('myfile' + str(cur))
      cur = cur + 1
      time.sleep(random.uniform(0.5,0.6))
      if (cur > 40):
        print 'reset'
        cur = 0
  finally:
    ftp.quit()
    time.sleep(random.uniform(0.5,0.6))
    print cur


