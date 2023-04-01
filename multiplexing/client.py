import socket

# create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the socket to the server's address and port
server_address = ('192.168.1.75', 5000) #hard coded
client_socket.connect(server_address)

# send "Hello World" to the server
message = "Hello World checking again"
client_socket.sendall(message.encode())

# receive the server's response
data = client_socket.recv(1024)
print("received: ", data.decode())

# close the socket
client_socket.close()
