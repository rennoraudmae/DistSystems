'''
Created on Sep 5, 2016

@author: devel
'''

from socket import AF_INET, SOCK_STREAM, socket

if __name__ == '__main__':
    print 'Application started'

    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'

    # No binding needed for client, OS will bind the socket automatically
    # when connect is issued

    server_address = ('127.0.0.1',7777)

    # Connecting ...
    s.connect(server_address)

    print 'Socket connected to %s:%d' % s.getpeername()
    print 'Local end-point is  bound to %s:%d' % s.getsockname()

    # Wait for user input before terminating application
    raw_input('Press Enter to terminate ...')

    s.close()
    print 'Terminating ...'