import socket
import struct
import sys


MULTICAST_GROUP = '224.0.0.1' # multicast group IP address
PORT = 5000      # multicast group port

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
receiver_socket.bind((MULTICAST_GROUP, PORT))

group_no = socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton('0.0.0.0')
mreq = struct.pack('4sL',group_no, socket.INADDR_ANY)

#receives datagram intented for multicast group using default interface
mreq2 = struct.pack('=4sl',socket.inet_aton(MULTICAST_GROUP),socket.INADDR_ANY)
#receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq2)

while True:
    data, address = receiver_socket.recvfrom(1024)
    print(f"Received data: {data.decode('utf-8')}")