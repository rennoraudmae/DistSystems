# Here we just keep the common session constants used by server and client
#
'''
Common variables, methods and structures of the MBoard modules
Created on Aug 23, 2016

@author: devel
'''
# Imports----------------------------------------------------------------------
from socket import SHUT_WR, SHUT_RD
from exceptions import Exception
# TCP related constants -------------------------------------------------------
#
DEFAULT_SERVER_PORT = 7777
DEFAULT_SERVER_INET_ADDR = '127.0.0.1'
#
# When receiving big messages in multiple blocks from the TCP stream
# the receive buffer size should be select according to amount of RAM available
# (more RAM = bigger blocks = less receive cycles = faster delivery)
TCP_RECEIVE_BUFFER_SIZE = 1024*1024
#
# MBoard protocol constants ---------------------------------------------------
#
# Copy-pasted from the UDP Application part2, removed everything related to the
# sessions protocol
#
# Added additional control routine __GET_N_LAST
# Since we can now send big messages, we may actually avoid splitting the
# routine "get last N messages" into 2 subroutines.
# We can do request and receive it at once
#
# @TODO: Control how much to store in memory
# Currently not controlled - big input may affect performance (swapping issue)
MAX_PDU_SIZE = 200*1024*1024 # Reasonable amount of data to store in RAM
# Requests --------------------------------------------------------------------
__REQ_PUBLISH = '1'
__REQ_LAST = '2'
__REQ_GET = '3'
__REQ_GET_N_LAST = '4'
__CTR_MSGS = { __REQ_GET:'Get message by id',
               __REQ_LAST:'Get iDs of last N messages',
               __REQ_PUBLISH:'Publish new message',
               __REQ_GET_N_LAST:'Get last N messages'
              }
# Responses--------------------------------------------------------------------
__RSP_OK = '0'
__RSP_BADFORMAT = '1'
__RSP_MSGNOTFOUND = '2'
__RSP_UNKNCONTROL = '3'
__RSP_ERRTRANSM = '4'
__RSP_CANT_CONNECT = '5'
__ERR_MSGS = { __RSP_OK:'No Error',
               __RSP_BADFORMAT:'Malformed message',
               __RSP_MSGNOTFOUND:'Message not found by iD',
               __RSP_UNKNCONTROL:'Unknown control code',
               __RSP_ERRTRANSM:'Transmission Error',
               __RSP_CANT_CONNECT:'Can\'t connect to server'
               }
# Field separator for sending multiple values ---------------------------------
__MSG_FIELD_SEP = ':'
# Exceptions ------------------------------------------------------------------
class MBoardProtocolError(Exception):
    '''Should be thrown internally on client or server while receiving the
    data, in case remote end-point attempts to not follow the MBoard protocol
    '''
    def __init__(self,msg):
        Exception.__init__(self,msg)
# Common methods --------------------------------------------------------------
def tcp_send(sock,data):
    '''Send data using TCP socket. When the data is sent, close the TX pipe
    @param sock: TCP socket, used to send/receive
    @param data: The data to be sent
    @returns integer,  n bytes sent and error if any
    @throws socket.errror in case of transmission error
    '''
    sock.sendall(data)
    sock.shutdown(SHUT_WR)
    return len(data)

def tcp_receive(sock,buffer_size=TCP_RECEIVE_BUFFER_SIZE):
    '''Receive the data using TCP receive buffer.
    TCP splits the big data into blocks automatically and ensures,
    that the blocks are delivered in the same order they were sent.
    Appending the received blocks into big message is usually done manually.
    In this method the receiver also expects that the sender will close
    the RX pipe after sending, denoting the end of sending
    @param buffer_size: integer, the size of the block to receive in one
            iteration of the receive loop
    @returns string, data received
    @throws socket.errror in case of transmission error,
            MBoard PDU size exceeded in case of client attempting to
            send more data the MBoard protocol allows to send in one PDU
            (MBoard request or response) - MAX_PDU_SIZE
    '''
    m = ''      # Here we collect the received message
    # Receive loop
    while 1:
        # Receive one block of data according to receive buffer size
        block = sock.recv(TCP_RECEIVE_BUFFER_SIZE)
        # If the remote end-point did issue shutdown on the socket
        # using  SHUT_WR flag, the local end point will receive and
        # empty string in all attempts of recv method. Therefore we
        # say we stop receiving once the first empty block was received
        if len(block) <= 0:
            break
        # There is no actual limit how big the message (m) can grow
        # during the block delivery progress. Still we have to take
        # into account amount of RAM on server when dealing with big
        # messages, and one point introduce a reasonable limit of
        # MBoard PDU (MBoard request/responses).
        if ( len(m) + len(block) ) >= MAX_PDU_SIZE:
            # Close the RX pipe to prevent the remote end-point of sending
            # more data
            sock.shutdown(SHUT_RD)
            # Garbage collect the unfinished message (m) and throw exception
            del m
            raise \
                MBoardProtocolError( \
                    'Remote end-point tried to exceed the MAX_PDU_SIZE'\
                    'of MBoard protocol'\
                )

        # Appending the blocks, assembling the message
        m += block
    return m