'''
Created on Apr 21, 2016

@author: Developer
'''

# From socket module we import the required structures and constants.
from socket import AF_INET, SOCK_STREAM, socket

if __name__ == '__main__':

    print 'Application started'

    # Creating a TCP/IP socket
    s = socket(AF_INET, SOCK_STREAM)

    # Binding the UDP/IP socket to address and port
    s.bind(('127.0.0.1',7777))
    print 'Socket is bound to %s:%d' % s.getsockname()

    # Turn the socket into listener-socket
    s.listen(0)
    print 'Socket is listening on %s:%d' % s.getsockname()

    # Wait for a client to connect
    client_socket,client_addr = s.accept()
    print 'Client connected from %s:%d' % client_addr

    # Receiving the message,
    # here we need to the socket API what is the size of the block
    # that we are ready to receive at once
    recv_buffer_length = 1024

    term = '\n'     # Terminator indicating the message is over
    message = ''    # This will grow in progress of receiving

    print 'Waiting for message ...'
    # Append message block by block till terminator is found
    while not message.endswith('\n'):
        m = client_socket.recv(recv_buffer_length)
        print 'Received block of %d from %s:%d'\
                '' % ( (len(m),) + client_socket.getpeername())
        message +=m

    print 'Total length %d bytes: [%s]' % (len(message),message)

    raw_input('Press Enter to terminate ...')

    client_socket.close()
    print 'Closed client socket...'
    s.close()
    print 'Closed the listener socket ...'
    print 'Terminating ...'
