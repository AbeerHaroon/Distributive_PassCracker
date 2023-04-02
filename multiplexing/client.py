import socket
import GuessGen
import sys
import ipaddress


SERVER_IP = "192.168.1.75"
SERVER_PORT = 5000

def printUsage():
    print("usage:")
    print("python3 client.py [temporary password] [IPv4 Address]")
    print("(optional)-p [number] sets a server port. default is 5000")

if len(sys.argv) != 3:
    printUsage()
    sys.exit()

#try catch block for checking port number. can be used for checking 
try:
    index_port = sys.argv.index("-p")
    x = int(sys.argv[index_port+1])
    if x >= 2000:
        SERVER_PORT = x
    else :
        print("minimum port value for server = 2000\nSetting up server in default port (5000)")
        SERVER_PORT = 5000
except ValueError as e:
    SERVER_PORT = 5000
    pass #do nothing

try:
    server_ip = sys.argv[2]
    x = ipaddress.IPv4Address(server_ip)
    SERVER_IP = x
except ValueError as e:
    print("please state valid server IP")
    sys.exit()
    pass #do nothing

message = sys.argv[1]
# create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the socket to the server's address and port
server_address = (SERVER_IP, SERVER_PORT) #hard coded
client_socket.connect(server_address)

# send secret message to the server
# message = "please_work"
client_socket.sendall(message.encode())

# receive the server's response
data = client_socket.recv(1024)
print("received: ", data.decode())

to_crack = data.decode()

g = GuessGen.GuessGen()
ans = g.crackCycle(to_crack) #bottleneck here most likely

client_socket.sendall(str(ans).encode())

# close the socket
client_socket.close()


