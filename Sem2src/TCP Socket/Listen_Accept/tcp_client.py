from socket import AF_INET, SOCK_STREAM, socket
if __name__=='__main__':
    print "App started"
    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'

    #No binding neede for client, Os will bind the socket automatically
    #when connection is issued
    server_address = ('127.0.0.1',7777)
    # Connecting ...
    s.connect(server_address)
    print 'Socket connected to %s:%d' % s.getpeername()
    print 'Local end-point is bound to %s:%d' % s.getsockname()
    #wait for user input before terminating application
    raw_input('Press Enter to terminate ...')
    s.close()
    print 'Terminating ...'
