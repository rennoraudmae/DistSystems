#!/usr/bin/python
#
# Implements message board TCP server
# -----------------------------------------------------------------------------
#
# Server is using static message board implementation and state-less
# implementation of message board protocol
# -----------------------------------------------------------------------------
#
# State-less protocol
#
# Switching to TCP protocol allows us to avoid programming of our own sessions
# for big-block delivery. TCP connections are in fact a data delivery sessions.
# Therefore in this implementation we just removed everything
# related to the sessions protocol, that we implemented for UDP.
# Also in the server part TCP,
# the listener socket is now defined, and accepting clients. We have still not
# introduced any threads, therefore our server can still handle only one client
# at once. In case of many clients connecting simultaneously we rely on backlog
# of the lister socket, which allows us to have a queue of connected clients
# (implemented in TCP protocol).
#
# Regarding the MBoard protocol itself and MBoard API we keep it untouched.
# -----------------------------------------------------------------------------
from tcp.mboard.sessions.server.protocol import __disconnect_client
'''
Message board server (TCP)
Created on Aug 19, 2016

@author: devel
'''
# Setup Python logging ------------------ -------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()
# Imports ---------------------------------------------------------------------
from tcp.mboard.sessions.server import protocol
from tcp.mboard.sessions import board
from tcp.mboard.sessions.common import tcp_receive, tcp_send, \
    MBoardProtocolError
from socket import socket, AF_INET, SOCK_STREAM
from socket import error as soc_error
from sys import exit
# Constants -------------------------------------------------------------------
___NAME = 'MBoard Server'
___VER = '0.1.0.0'
___DESC = 'Simple Message Board Server (TCP version)'
___BUILT = '2016-09-13'
___VENDOR = 'Copyright (c) 2016 DSLab'
# -----------------------------------------------------------------------------
# How many clients may there be awaiting to get connection if the server is
# currently busy processing the other request
__DEFAULT_SERVER_TCP_CLIENTS_QUEUE = 10
# Private methods -------------------------------------------------------------
def __info():
    return '%s version %s (%s) %s' % (___NAME, ___VER, ___BUILT, ___VENDOR)
# Not a real main method-------------------------------------------------------
def mboard_server_main(args):
    '''Runs the Mboard server
    should be run by the main mehtod of CLI or GUI application
    @param args: ArgParse collected arguments
    '''
    # Starting server
    LOG.info('%s version %s started ...' % (___NAME, ___VER))
    LOG.info('Using %s version %s' % ( protocol.___NAME, protocol.___VER))
    LOG.info('Using %s version %s' % ( board.___NAME, board.___VER))

    # Declaring TCP socket
    __server_socket = socket(AF_INET,SOCK_STREAM)
    LOG.debug('Server socket created, descriptor %d' % __server_socket.fileno())
    # Bind TCP Socket
    try:
        __server_socket.bind((args.listenaddr,int(args.listenport)))
    except soc_error as e:
        LOG.error('Can\'t start MBoard server, error : %s' % str(e) )
        exit(1)
    LOG.debug('Server socket bound on %s:%d' % __server_socket.getsockname())
    # Put TCP socket into listening state
    __server_socket.listen(__DEFAULT_SERVER_TCP_CLIENTS_QUEUE)
    LOG.info('Accepting requests on TCP %s:%d' % __server_socket.getsockname())

    # Declare client socket, set to None
    client_socket = None

    # Serve forever
    while 1:
        try:
            LOG.debug('Awaiting new client connections ...')
            # Accept client's connection store the client socket into
            # client_socket and client address into source
            client_socket,source = __server_socket.accept()
            LOG.debug('New client connected from %s:%d' % source)

            # Start receiving the blocks appending the data into message (m)
            # The TCP does deliver the big messages in blocks and ensures
            # the order of the blocks. All is left to do is to append the
            # the blocks into a message when receiving.
            # Since we are dealing here with the stream we should be able
            # to distinguish where is the end of the message
            # We could introduce some terminator character for example, but
            # we don't have to. TCP already implements routines like
            # socket shutdown for closing RX or TX pipes of the TCP socket.
            # Shutdown routine however does not affect the I/O descriptor
            # assigned to a socket. The I/O descriptor should closed using
            # close method. TCP Socket shutdown flags:
            # SHUT_WR: sending is over - you may stop receiving now
            # SHUT_RD: receiving is over - stop sending the data
            #
            m = ''      # Here we collect the received message
            try:
                m = tcp_receive(client_socket)
            except (soc_error, MBoardProtocolError) as e:
                # In case we failed in the middle of transfer we should report error
                LOG.error('Interrupted receiving the data from %s:%d, '\
                          'error: %s' % (source+(e,)))
                # ... and close socket
                __disconnect_client(client_socket)
                client_socket = None
                # ... and proceed to next client waiting in to accept
                continue

            # In case message (m) has less then bare minimal of Mboard
            # protocol PDU ( 1 control char and delimiter ),
            # we definitely do not want to server this kind of client ...
            if len(m) <=  2:
                __disconnect_client(client_socket)
                client_socket = None
                # ... and we should proceed to the others
                continue

            # Now here we assumen the message contains
            LOG.debug('Received message [%d bytes] '\
                      'from %s:%d' % ((len(m),)+source))
            # Issue MBoard protocol to process the
            # request message (m) send from the client (source)
            r = protocol.server_process(board, m, source)
            # Try to send the response (r) to client
            # Shutdown the TX pipe of the socket after sending
            try:
                LOG.debug('Processed request for client %s:%d, '\
                          'sending response' % source)
                # Send all data of the response (r)
                tcp_send(client_socket, r)
            except soc_error as e:
                # In case we failed in the middle of transfer we should report error
                LOG.error('Interrupted sending the data to %s:%d, '\
                          'error: %s' % (source+(e,)))
                # ... and close socket
                __disconnect_client(client_socket)
                client_socket = None
                # ... and we should proceed to the others
                continue

            # At this point the request/response sequence is over, we may
            # close the client socket and proceed to the next client
            __disconnect_client(client_socket)
            client_socket=None


        except KeyboardInterrupt as e:
            LOG.debug('Crtrl+C issued ...')
            LOG.info('Terminating server ...')
            break

    # If we were interrupted, make sure client socket is also closed
    if client_socket != None:
        __disconnect_client(client_socket)

    # Close server socket
    __server_socket.close()
    LOG.debug('Server socket closed')