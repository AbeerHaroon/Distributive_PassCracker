import select
import socket
import sys
import GuessGen

SERVER_PORT = 5000
unlock_pw = "please"

if len(sys.argv) < 3 :
    print("please print number of machines being used")
    print("each username after (third argument)")
    print("(considering program name first arg)")
    sys.exit()

numConnections = int(sys.argv[1])
if numConnections > 10 :
    print("maximum 10 connections")
    sys.exit()

# users = [] #List of users to crack
# numUsers = 1
# while(numUsers < len(sys.argv)):
#     users.append(sys.argv[numUsers])
#     numUsers +=1
#     #List of users added

# hashed_passes = []

# for u in users:
#     #Module that will search for username in command line
#     with open('/etc/shadow') as f:
#         line = f.read()
#         print(line)
#         uName_Index = line.find(u)
#         if uName_Index != -1: #if username found
#             passIndexFirst = len(u) + 1
#             chop = line[uName_Index+(passIndexFirst):] #starting from first index where username found + add up to index of when pass starts 
#             colonAfterPass = chop.find(":") #find index of first occurrence of colon
#             hashed = chop[0:colonAfterPass] #excluded colon index
#             print("extracted hash:",end="")
#             print(hashed)
#             hashed_passes.append(hashed)

# solved_passes = []
# print("following hashed passwords found")
# print(hashed_passes)

# if len(hashed_passes) == 0:
#     print("no hash pass found")
#     sys.exit()
 
# to_crack = hashed_passes[0] #first password found for now
to_crack = "$y$j9T$oHjB961YNYYZaS/B9V5sr1$eqVAPSL4NpprMtfP9ie6jayp.rdiGsdFQPa/KRVOxm7" #yescrypt for 2!

# create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to a specific address and port
server_address = ('0.0.0.0', SERVER_PORT)
server_socket.bind(server_address)

# listen for incoming connections
server_socket.listen(numConnections)

# create a list of sockets to monitor for incoming data
inputs = [server_socket]

while True:
    #utilizes the inputs List() above. List of sockets 
    # use the select module to monitor the list of sockets for incoming data
    readable, writable, exceptional = select.select(inputs, [], [])

    #iterate through the sockets that have data
    for sock in readable: #there is activity in readable
        if sock is server_socket:
            # accept incoming connection
            connection, client_address = sock.accept()
            connection.setblocking(0)
            inputs.append(connection)
        else:
            # receive incoming data
            data = sock.recv(1024)
            if data.decode() == unlock_pw:
                print("recognized temp pass from client")
                # echo the data back to the client
                sock.sendall(to_crack.encode())
            else:
                # close the socket
                sock.close()
                inputs.remove(sock)
