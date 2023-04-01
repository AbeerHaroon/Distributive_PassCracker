import socket

MULTICAST_GROUP = '225.4.2.0' # multicast group IP address
PORT = 5000      # multicast group port

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver_socket.bind(('', PORT))
mreq = socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton('0.0.0.0')
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    data, address = receiver_socket.recvfrom(1024)
    print(f"Received data: {data.decode('utf-8')}")