'''
Starter Script for MBoard Client CLI application
Created on Sep 14, 2016

@author: devel
'''
# Imports----------------------------------------------------------------------
from tcp.mboard.sessions.client.main import __info, ___VER,\
    mboard_client_main
from tcp.mboard.sessions.common import DEFAULT_SERVER_INET_ADDR,\
    DEFAULT_SERVER_PORT
from argparse import ArgumentParser # Parsing command line arguments
from sys import path,argv
from os.path import abspath, sep
# Main method -----------------------------------------------------------------
if __name__ == '__main__':
    # Find the script absolute path, cut the working directory
    a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
    path.append(a_path)
    # Parsing arguments
    parser = ArgumentParser(description=__info(),
                            version = ___VER)
    parser.add_argument('-H','--host',\
                        help='Server INET address '\
                        'defaults to %s' % DEFAULT_SERVER_INET_ADDR, \
                        default=DEFAULT_SERVER_INET_ADDR)
    parser.add_argument('-p','--port', type=int,\
                        help='Server UDP port, '\
                        'defaults to %d' % DEFAULT_SERVER_PORT, \
                        default=DEFAULT_SERVER_PORT)
    parser.add_argument('-m','--message',\
                        help='Message to publish',\
                        default='')
    parser.add_argument('-l','--last', metavar='N', type=int,\
                        help='Get iDs of last N messages,'\
                        'defaults to "all"',\
                        default=0)
    args = parser.parse_args()
    # Run Mboard Client
    mboard_client_main(args)