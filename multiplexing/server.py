import select
import socket

# create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to a specific address and port
server_address = ('0.0.0.0', 5000)
server_socket.bind(server_address)

# listen for incoming connections
server_socket.listen(5)

# create a list of sockets to monitor for incoming data
inputs = [server_socket]

while True:
    # use the select module to monitor the list of sockets for incoming data
    readable, writable, exceptional = select.select(inputs, [], [])

    #iterate through the sockets that have data
    for sock in readable:
        if sock is server_socket:
            # accept incoming connection
            connection, client_address = sock.accept()
            connection.setblocking(0)
            inputs.append(connection)
        else:
            # receive incoming data
            data = sock.recv(1024)
            if data:
                # echo the data back to the client
                sock.sendall(data)
            else:
                # close the socket
                sock.close()
                inputs.remove(sock)
