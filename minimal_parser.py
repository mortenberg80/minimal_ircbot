# -*- coding: utf-8 -*-
import sys
import datetime as dt

import config

input = sys.stdin.readline()

message = []

if input == "ping":
    message = "Hei hei!"
elif input.startswith(config.NICK):
    to_message = input[len(config.NICK):].lstrip()
    print to_message
    message = "Beklager... Jeg har ikke lært å snakke ennå :("
elif input == "time":
    message = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

if type(message) == str:
    message = message.split('\n')

for message_line in message:
    print message_line
