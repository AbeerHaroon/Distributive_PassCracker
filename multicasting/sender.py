import socket
import struct
import sys

MULTICAST_GROUP = '225.4.2.0' # multicast group IP address
PORT = 5000      # multicast group port
msg = b"Hello, World!"

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
ttl = struct.pack('b',2)
sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

sender_socket.sendto(msg, (MULTICAST_GROUP, PORT))