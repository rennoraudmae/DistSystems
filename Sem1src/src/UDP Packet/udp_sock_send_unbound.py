from socket import AF_INET, SOCK_DGRAM, socket

if __name__ == '__main__':

    print 'Application started'

    # Creating a UDP/IP socket
    s = socket(AF_INET, SOCK_DGRAM)

    # Sending the message (socket is still unbound)
    message = 'Hell world!'
    destination = ('127.0.0.1',7778)
    s.sendto(message,destination)
    print 'Sent message to %s:%d' % destination
    print 'Payload lengh %d bytes: [%s]' % (len(message),message)

    # Let's check how the socket API did bind the socket
    print 'Socket was automatically bound to %s:%d' % s.getsockname()

    raw_input('Press Enter to teminate ...')

    print 'Closing the UDP socket ...'
    s.close()
    print 'Terminating ...'
