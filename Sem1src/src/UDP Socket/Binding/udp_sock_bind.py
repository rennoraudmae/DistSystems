'''
Created on Apr 21, 2016

@author: Developer
'''

# From socket module we import the required structures and constants.
from socket import AF_INET, SOCK_DGRAM, socket
# And we also will need the process id given by OS when we execute this code
from os import getpid

if __name__ == '__main__':

    print 'Application started'
    print 'OS assigned process id: %d' % getpid()

    # Creating a UDP/IP socket
    s = socket(AF_INET, SOCK_DGRAM)
    print 'UDP Socket created'
    print 'File descriptor assigned by OS: ', s.fileno()

    # Binding the UDP/IP socket to address and port
    s.bind(('127.0.0.1', 0))
    print 'Socket is bound to %s:%d' % s.getsockname()

    raw_input('Press Enter to teminate ...')

    print 'Closing the UDP socket ...'
    s.close()
    print 'Terminating ...'
