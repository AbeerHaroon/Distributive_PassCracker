import socket
import GuessGen
import sys

SERVER_IP = '192.168.1.75'
message = sys.argv[1]
# create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the socket to the server's address and port
server_address = (SERVER_IP, 5000) #hard coded
client_socket.connect(server_address)

# send secret message to the server
# message = "what_is_love"
client_socket.sendall(message.encode())

# receive the server's response
data = client_socket.recv(1024)
print("received: ", data.decode())

to_crack = data.encode()

g = GuessGen.GuessGen()
ans = g.crackCycle(to_crack)

client_socket.sendall(str(ans).encode())

# close the socket
client_socket.close()