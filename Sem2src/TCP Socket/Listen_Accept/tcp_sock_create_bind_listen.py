from socket import AF_INET, SOCK_STREAM, socket
from os import getpid

if __name__ == '__main__':
    print 'Application started'
    print 'OS assigned process id: %d' % getpid()

    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'
    print 'File descriptor assigned by OS: ', s.fileno()
    # Binding the TCP/IP socket to loop-back address and port 7777
    s.bind(('127.0.0.1',7778))
    print 'Socket is bound to %s:%d' % s.getsockname()

    # Put socket into listening state
    backlog = 0 # Waiting queue size, 0 means no queue
    s.listen(backlog)

    print 'Socket %s:%d is in listening state' % s.getsockname()

    # Wait for user input before terminating application
    raw_input('Press Enter to terminate ...')

    s.close()
    print 'Terminating ...'
