import ftplib
import sys
import os

def downloadFile(ftp, fileName):

    ftp.retrbinary('RETR ' + fileName, open(fileName, 'wb').write, 1024)
	
 
for i in range(100):
  ftp = ftplib.FTP('127.0.0.1') #I hope it works.
  ftp.login('msfadmin','msfadmin')
# CHANGE DIR?
  downloadFile(ftp, 'myfile.txt')
  ftp.quit()
  sleep(1)
