# -*- coding: utf-8 -*-
# Based on the O'Reilly example at http://oreilly.com/pub/h/1968
import sys
import socket
import subprocess

import config

readbuffer=''

s=socket.socket()
s.connect((config.HOST, config.PORT))
s.send("NICK %s\r\n" % config.NICK)
s.send("USER %s %s bla :%s\r\n" % (config.IDENT, config.HOST, config.REALNAME))
s.send("JOIN %s\r\n" % config.CHANNEL)

print 'Running'

def parse(input):
    p = subprocess.Popen(config.PARSE_COMMAND,
        shell=True,
        bufsize=1024,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)

    return p.communicate(input=input)[0].strip().split('\n')

while 1:
    readbuffer = readbuffer + s.recv(1024)
    temp = readbuffer.split("\n")
    readbuffer = temp.pop()

    for line in temp:
        line = line.strip()
        tokens = line.split()

        if tokens[1] == "PRIVMSG" and tokens[2] == config.CHANNEL:
            messages = parse(line)
            for message in messages:
                s.send("PRIVMSG %s :%s\r\n" % (config.CHANNEL, message))

        if line[0] == "PING":
            s.send("PONG %s\r\n" % tokens[1])
