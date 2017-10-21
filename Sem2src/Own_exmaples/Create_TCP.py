from socket import AF_INET, SOCK_STREAM, socket

from time import sleep

from os import getpid

if __name__=='__main__':
    print 'Application start!'
    print 'Os assigned process id: %d' % getpid()
    # creating a TCP/IP socket
    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'

    print 'File descriptor assigned by OS: ', s.fileno ()

    s.bind(('127.0.0.1',7777))
    print 'Socket is bound to %s:%d' % s.getsockname()

    backlog = 0
    s.listen(backlog)
    #wait for user input before terminating application

    raw_input("Press Enter to terminate ...")

    s.close()
    print 'Terminating ...'


