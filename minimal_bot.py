# -*- coding: utf-8 -*-
import sys
import socket
import string
import subprocess

import config

readbuffer=''

s=socket.socket()
s.connect((config.HOST, config.PORT))
s.send("NICK %s\r\n" % config.NICK)
s.send("USER %s %s bla :%s\r\n" % (config.IDENT, config.HOST, config.REALNAME))
s.send("JOIN %s\r\n" % config.CHANNEL)

def parse(string):
    p = subprocess.Popen('python %s' % 'minimal_parser.py', shell=True, bufsize=1024, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    try:
        p.stdin.writelines(string)
    finally:
        p.stdin.close()

    return p.stdout.readlines()

print 'Running'

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop()

    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)

        if line[1] == "PRIVMSG" and line[2] == config.CHANNEL:
            messages = parse(line[3][1:])
            for message in messages:
                s.send("PRIVMSG %s :%s\r\n" % (config.CHANNEL, message))

        if line[0]=="PING":
            s.send("PONG %s\r\n" % line[1])
