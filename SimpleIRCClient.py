import socket
import time
import random

server_ip = 'localhost'
server_port = 6667
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server_ip, server_port))
botnick = 'bot1'
irc.send("USER " + botnick + " 127.0.0.1 " + botnick + " :This is a fun bot!\n")   # user authentication
irc.send("NICK " + botnick + "\n")
channel = '#testit'
irc.send("JOIN " + channel + "\n")  # join the chan

while True:
  
  time.sleep(4)
  irc.send("PRIVMSG  " + channel + " Hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii" + "\n")  # join the chan
  #time.sleep(3)
  irc.send("PRIVMSG  " + channel + " BLABLALBLALBLALBLALBLALBLALBLALABLLALBLA" + "\n")  # join the chan
  #time.sleep(3)
  irc.send("PRIVMSG  " + channel + " ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "\n")  # join the chan
  #time.sleep(3)
  irc.send("PRIVMSG  " + channel + " ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ" + "\n")  # join the chan
  time.sleep(random.random() * 4)


