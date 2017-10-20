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
    s.bind(('127.0.0.1',7777))
    print 'Socket is bound to %s:%d' % s.getsockname()

    # Sending the message
    message = 'Hell world!'
    destination = ('127.0.0.1',7778)
    s.sendto(message,destination)
    print 'Sent message to %s:%d' % destination
    print 'Payload lengh %d bytes: [%s]' % (len(message),message)

    raw_input('Press Enter to teminate ...')

    print 'Closing the UDP socket ...'
    s.close()
    print 'Terminating ...'
