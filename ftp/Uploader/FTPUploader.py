import ftplib
import sys
import os


def uploadFile(ftp, filename) :
  ftp.storbinary("STOR " + filename, open(filename), 1024)



for i in range(100):
  ftp = ftplib.FTP('127.0.0.1') #I hope it works.
  ftp.login('msfadmin', 'msfadmin')
  # CHANGE DIR?
  filename = 'myfile.txt'
  uploadFile(ftp, filename)
  ftp.quit()
  sleep(1)






	
	
	
	