'''
Created on Apr 22, 2016

@author: Developer
'''

# From socket module we import the required structures and constants.
from socket import AF_INET, SOCK_STREAM, socket
# Sleep function will be used to keep application running for a while
from time import sleep
# And we also will need the process id given by OS when we execute this code
from os import getpgid
from posix import getpid

if __name__ == '__main__':

    print 'Application started'
    print 'OS assigned process id: %d' % getpid()

    # Creating a UDP/IP socket
    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'
    print 'File descriptor assigned by OS: ', s.fileno()

    wait_secs = 60*5

    print 'Waiting %d seconds before termination ...' % wait_secs
    sleep(wait_secs)

    print 'Closing the TCP socket ...'
    s.close()
    print 'Terminating ...'