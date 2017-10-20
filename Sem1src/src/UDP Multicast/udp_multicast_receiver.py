#!/usr/bin/python
#
# Implements Python UDP multicast receiver
#
# Based on the code from:
# http://stackoverflow.com/questions/603852/multicast-in-python

'''Simple UDP Multicast receiver
    @author: devel
'''
# Tired of print ------------------ -------------------------------------------
# ... setup Python logging as defined in:
# https://docs.python.org/2/library/logging.html
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()
# Needed imports --------------------------------------------------------------

# Socket
from socket import socket
# Socket attributes
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SOL_IP
from socket import IPPROTO_IP, IP_MULTICAST_LOOP, IP_DEFAULT_MULTICAST_TTL
from socket import inet_aton, IP_ADD_MEMBERSHIP

# Constants  ------------------------------------------------------------------

# The multi-cast group address we are going to use
__mcast_addr = '237.1.1.1'

# The multi-cast group port
__mcast_port = 53124

# The multi-cast time-to-live (router hops)
__mcast_ttl = 4

# Receiving buffer
__mcast_buffer = 1024

# Initialization  -------------------------------------------------------------

# Declare UDP socket
__s = socket(AF_INET, SOCK_DGRAM)
LOG.debug('UDP socket declared ...')

# Reusable UDP socket? I am not sure we really need it ...
__s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
LOG.debug('UDP socket reuse set ...')

# Enable loop-back multi-cast - the local machine will also receive multicasts
__s.setsockopt(IPPROTO_IP,IP_MULTICAST_LOOP,1)
LOG.debug('Enabled loop-back multi-casts ...')

# Set multi-cast time-to-live, let say we go up 4 sub-nets
__s.setsockopt(IPPROTO_IP, IP_DEFAULT_MULTICAST_TTL, __mcast_ttl)
LOG.debug('Set multi-cast time-to-live [%d] hops ...', __mcast_ttl)

# Bind UDP socket to listen to muli-casts
__s.bind((__mcast_addr,__mcast_port))
LOG.debug('Socket bound to %s:%s' % __s.getsockname())

__s.setsockopt(SOL_IP, IP_ADD_MEMBERSHIP, \
               inet_aton(__mcast_addr) + inet_aton('0.0.0.0'))

# Receiving -------------------------------------------------------------------

# Listen forever (Ctrl+C) to kill
while 1:
    try:
        # Receive multi-cast message
        message,addr = __s.recvfrom(__mcast_buffer)
        LOG.debug('Received From: %s:%s [%s]' % (addr+(message,)))

    except (KeyboardInterrupt, SystemExit) as e:
        LOG.info('Terminating client ...\n')
        break

# Termination -----------------------------------------------------------------
# Clean-up the socket
__s.close()
LOG.debug('Socket closed ...')
LOG.info("Server terminated ...")
