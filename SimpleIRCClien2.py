import socket
import time

server_ip = 'localhost'
server_port = 6667
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server_ip, server_port))
botnick = 'bot2'
irc.send("USER " + botnick + " 127.0.0.1 " + botnick + " :This is a fun bot!\n")   # user authentication
irc.send("NICK " + botnick + "\n")
channel = '#testit'
irc.send("JOIN " + channel + "\n")  # join the chan

while True:
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text
  text = irc.recv(200)   # join the chan
  print text