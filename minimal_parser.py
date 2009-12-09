# -*- coding: utf-8 -*-
import sys
import datetime as dt

import config

class parser:
    def __init__(self, input):
        self.input = input
        self.tokens = input.split()
        self.message_tokens = self.tokens[3:]
        self.message_tokens[0] = self.message_tokens[0][1:]

    def parse(self):
        message = ' '.join(self.message_tokens)
        output = []

        if message.lower() == "ping":
            output = self.handle_ping()

        elif message.lower() == "time":
            output = self.handle_time()

        elif self.message_tokens.pop(0) == '%s:' % config.NICK:
            output = self.parse_personal_message()

        if type(output) == str:
            output = output.split('\n')

        return output

    def parse_personal_message(self):
        self.message = ' '.join(self.message_tokens)

        if self.message.lower() == 'how are you?':
            return self.handle_personal_how_are_you()
        else:
            output = ["Beklager... Jeg har ikke lært meg ditt språk ennå."]
            output += ["Prøv %s: how are you?" % config.NICK]
            return output

    def handle_personal_how_are_you(self):
        return 'I am bad to the bone!'

    def handle_ping(self):
        return 'pong'

    def handle_time(self):
        return dt.datetime.now().strftime("%Y-%m-%d %H:%M")

p = parser(sys.stdin.readline())
output = p.parse()

for output_line in output:
    print output_line
