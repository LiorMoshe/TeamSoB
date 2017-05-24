import ftplib
import sys
import os
import time
import random

def uploadFile(ftp, filename) :
  ftp.storbinary("STOR " + filename, open(filename), 1024)


cur = 0
filename = 'myfile0'
while(True):
  ftp = ftplib.FTP('127.0.0.1') #I hope it works.
  try :
    ftp.login('msfadmin', 'msfadmin')   
    for j in range(random.randint(0, 15)):
      os.rename(filename, filename[0:6] + str(cur))
      filename = filename[0:6] + str(cur)
      uploadFile(ftp, filename)
      cur = cur + 1
      if (cur > 40):
        print 'reset'
        cur = 0
      time.sleep(random.uniform(0.5,0.55))
    if (random.randint(0, 1) > 0):
      if (random.randint(0,1) > 0):
        if (random.randint(0,1) > 0):
          ftp.nlst()
  finally :
    ftp.quit()
    time.sleep(random.uniform(0.5, 0.55))






	
	
	
	