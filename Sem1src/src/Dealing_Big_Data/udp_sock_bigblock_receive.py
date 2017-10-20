'''
Created on Apr 21, 2016

@author: Developer
'''

# From socket module we import the required structures and constants.
from socket import AF_INET, SOCK_DGRAM, socket

if __name__ == '__main__':

    print 'Application started'

    # Creating a UDP/IP socket
    s = socket(AF_INET, SOCK_DGRAM)

    # Binding the UDP/IP socket to address and port
    s.bind(('127.0.0.1',7778))
    print 'Socket is bound to %s:%d' % s.getsockname()

    # Receiving the message, maximal pay-load to receive in one peace
    recv_buffer_length = 1024

    term = '\n'     # Terminator indicating the message is over
    message = ''    # This will grow in progress of receiving

    print 'Waiting for message ...'
    # Append message block by block till terminator is found
    while not message.endswith('\n'):
        m,source = s.recvfrom(recv_buffer_length)
        print 'Received block of %d from %s:%d' % ( (len(m),) +source)
        message +=m

    print 'Total lengh %d bytes: [%s]' % (len(message),message)

    raw_input('Press Enter to teminate ...')

    print 'Closing the UDP socket ...'
    s.close()
    print 'Terminating ...'
