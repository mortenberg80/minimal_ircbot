HOST = 'irc.homelien.no'
PORT = 6667
NICK = 'mynick'
IDENT = 'pybot'
REALNAME = 'I am'
CHANNEL = '#mychannel'
PARSE_COMMAND = 'python ./minimal_parser.py'

try:
    from local_config import *
except ImportError:
    pass
