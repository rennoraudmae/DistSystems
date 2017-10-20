from socket import AF_INET, SOCK_STREAM,  socket

if __name__ == '__main__':

    print 'Application started'

    # Creating a UDP/IP socket
    s = socket(AF_INET, SOCK_STREAM)

    # Sending the message (socket is still unbound)
    # We will use the break line to indicate the end of message
    # then the receiver may receive without knowing the full length
    # of the message he is receiving
    term = '\n'
    message = 'Hell world!'*7000+term

    destination = ('127.0.0.1',7777)

    # Connect to the server
    s.connect(destination)
    print 'Connected to the server %s:%d' % s.getpeername()
    print 'Local end-point bound on %s:%d' % s.getsockname()

    # Send the data

    s.sendall(message)

    print 'Sent message to %s:%d' % destination
    print 'Pay-load length %d bytes: [%s]' % (len(message),message)

    raw_input('Press Enter to terminate ...')

    print 'Closing the TCP socket ...'
    s.close()
    print 'Terminating ...'
