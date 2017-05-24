import ftplib
import sys
import os
import time

def uploadFile(ftp, filename) :
  ftp.storbinary("STOR " + filename, open(filename), 1024)


filename = 'myfile0'
for i in range(100):
  ftp = ftplib.FTP('127.0.0.1') #I hope it works.
  ftp.login('msfadmin', 'msfadmin')
  # CHANGE DIR?
  os.rename(filename, filename[0:6] + str(i))
  filename = filename[0:6] + str(i)
  uploadFile(ftp, filename)
  ftp.quit()
  time.sleep(1)






	
	
	
	