#!/usr/bin/python
#
# Implements Python UDP multicast sender
#
# Based on the code from:
# http://stackoverflow.com/questions/603852/multicast-in-python

'''Simple UDP Multicast sender
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
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from socket import IPPROTO_IP, IP_MULTICAST_LOOP, IP_DEFAULT_MULTICAST_TTL
#
from time import sleep

# Constants  ------------------------------------------------------------------

# The multi-cast group address we are going to use
__mcast_addr = '237.1.1.1'

# The multi-cast group port
__mcast_port = 53124

# The multi-cast time-to-live (router hops)
__mcast_ttl = 4

# Broadcast interval seconds
__mcast_delay = 5

# Particular message the server sends to identify himself
__mcast_message = u'Hell World!'

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
LOG.debug('Set multicast time-to-live [%d] hops ...', __mcast_ttl)

# For multi-casting we do not need any specific bindings
# ... socket will be bound automatically to interface with sub-net providing
# default gateway, the port will be also defined randomly

# Serving ---------------------------------------------------------------------

# Server forever (Ctrl+C to kill)
__n = 0
while 1:
    try:
        # Send out multi-cast message
        __s.sendto(__mcast_message, (__mcast_addr, __mcast_port))
        __n += 1
        LOG.debug('[%d] Multi-cast sent ...', __n)
        sleep(__mcast_delay)
    except (KeyboardInterrupt, SystemExit) as e:
        LOG.info('Terminating server ...\n')
        break

# Termination -----------------------------------------------------------------
# Clean-up the socket
__s.close()
LOG.debug('Socket closed ...')
LOG.info("Server terminated ...")
