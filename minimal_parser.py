# -*- coding: utf-8 -*-
import datetime as dt
import re
import subprocess
import sys

import config

class Parser(object):
    def __init__(self, input):
        self.input = input
        self.input_tokens = input.split()
        self.tokens = self.input_tokens[3:]
        self.tokens[0] = self.tokens[0][1:]

    def parse(self):
        message = ' '.join(self.tokens)
        output = []

        if self.tokens[0] == '%s:' % config.NICK:
            self.tokens.pop(0)
            handler_name = self.find_handler(prefix = 'handle_personal')
        else:
            handler_name = self.find_handler(prefix = 'handle')

        try:
            output = apply(self.__getattribute__(handler_name))
        except AttributeError:
            pass

        if type(output) == str:
            output = output.strip().split('\n')

        return output

    def find_handler(self, parser=None, prefix = 'handle', default = 'default'):
        if parser is None:
            parser = self

        handler_name = prefix
        while len(self.tokens) > 0:
            token = self.tokens.pop(0)

            search = ''.join(re.findall('\w', token.lower()))
            handler_name += '_%s' % search

            if hasattr(parser, handler_name):
                return handler_name

        return '%s_%s' % (prefix, default)

    def handle_ping(self):
        return 'pong'

    def handle_time(self):
        return dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    def handle_personal_default(self):
        output = ["Beklager... Jeg har ikke lært meg ditt språk ennå."]
        output += ["Prøv %s: how are you?" % config.NICK]
        return output

    def handle_personal_how_are_you(self):
        return 'I am bad to the bone!'

    def handle_personal_echo(self):
        return ' '.join(self.tokens)

    def handle_personal_ping(self):
        host = self.tokens.pop(0)
        try:
            re.match('^\w[\w\.]+\w$', host).group(0)
            p = subprocess.Popen(["ping", "-c 1", host],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
            error = p.stderr.readline()
            if len(error) > 0:
                return error
            else:
                return p.stdout.readlines()[1]
        except AttributeError:
            return "Example usage: %s: ping vg.no" % config.NICK

p = Parser(sys.stdin.readline())
output = p.parse()

for output_line in output:
    print output_line
