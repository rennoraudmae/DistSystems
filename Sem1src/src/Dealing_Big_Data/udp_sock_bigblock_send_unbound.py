from socket import AF_INET, SOCK_DGRAM,  socket

if __name__ == '__main__':

    print 'Application started'

    # Creating a UDP/IP socket
    s = socket(AF_INET, SOCK_DGRAM)

    # Sending the message (socket is still unbound)
    # We will use the break line to indicate the end of message
    # then the receiver may receive without knowing the full length
    # of the message he is receiving
    term = '\n'
    message = 'Hell world!'*7000+term

    max_len = 1024 # Maximal pay-load size to send in one UDP packet
    destination = ('127.0.0.1',7778)

    # In case there is more data, send it in peaces
    m = message # this will be reduced in progress of sending
    sent = 0    # how much was sent
    parts = 0   # count total sent packets

    # Cut the message into blocks and send out till the message is over
    while sent < len(message):
        m_send = m[:max_len] if len(m) > max_len else m
        m = m[max_len:]
        sent += s.sendto(m_send,destination)
        parts += 1
        print 'Sent %d bytes of %d ...' % (sent,len(message))

    print 'Sent message to %s:%d in %d parts' % (destination + (parts,))
    print 'Pay-load length %d bytes: [%s]' % (len(message),message)

    raw_input('Press Enter to terminate ...')

    print 'Closing the UDP socket ...'
    s.close()
    print 'Terminating ...'
