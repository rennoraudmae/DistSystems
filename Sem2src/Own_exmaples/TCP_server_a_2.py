
from socket import AF_INET, SOCK_STREAM, socket

if __name__ == '__main__':
    print 'Application started'

    s = socket(AF_INET, SOCK_STREAM)
    print 'TCP Socket created'
    # Binding the TCP/IP socket to loop-back address and port 7777
    s.bind(('127.0.0.1',7779))
    print 'Socket is bound to %s:%d' % s.getsockname()

    # Put socket into listening state
    backlog = 0 # Waiting queue size, 0 means no queue
    s.listen(backlog)

    print 'Socket %s:%d is in listening state' % s.getsockname()

    client_socket,client_addr = s.accept()
    print 'New client connected from %s:%d' % client_addr
    print 'Local end-point socket bound on: %s:%d'\
            '' % client_socket.getsockname()

    # Once the client is connected start receiving the data using its socket:
    recv_buffer_length = 1024
    message = client_socket.recv(recv_buffer_length)
    print 'Received %d bytes from %s:%d' % ( (len(message),)+client_addr )
    print 'Received message: \n%s' %  message

    # Wait for user input before terminating application
    raw_input('Press Enter to terminate ...')

    client_socket.close()
    print 'Closed the client socket'

    s.close()
    print 'Closed the server socket'
    print 'Terminating ...'
