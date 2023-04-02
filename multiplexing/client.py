import socket
import GuessGen
import sys
import ipaddress
import HashGuesser
import os
import string

SERVER_IP = "192.168.1.75"
SERVER_PORT = 5000
single = 0 # if 1, single thread will be used
multi = 0 # if 1, multi thread will be used #TODO Cracker from Sepehr_Cracker potentially

#sepehrman:$y$j9T$.Ciip2iHePTF7RvA1q3rX0$OeW1icDofEhPQhV4jPStlhsxPOmqmNcZlgaEfaXezE0:19381:0:99999:7:::\n'
def parseHash(fullHash):
    usernameIndex = fullHash.find(":") #find instance of first :
    minus_user = fullHash[usernameIndex+1:] #extract string starting from hash to end
    last_colon = minus_user.find(":") #find index of next colon
    extract_hash = minus_user[0:last_colon] #extract from beginning hash to colon (excluding)
    return extract_hash

def printUsage():
    print(" usage: (ORDER MATTERS)")
    print("\tpython3 client.py [a number] [IPv4 Address] [\'-s\' OR \'-m\']\n")
    print("\t a number -  the index of the hash in the server.\n",
          "\t             server has a list of hashes, we can ask for a specific index from the list\n",
          "\t             (0 is first)")
    print("\t-s - chooses single threaded cracker (predictable guess generation)")
    print("\t-m - chooses multi threaded cracker (unpredictable guess generation)\n")
    print("\t(optional)-p [number] sets a server port. default is 5000\n")

if len(sys.argv) < 4:
    printUsage()
    sys.exit()

if sys.argv[3] == "-s":
    single = 1
elif sys.argv[3] == "-m":
    print("Chosen multi-threaded cracker")
    print("Be advised, multi-threaded cracker is buggy and testing is not complete")
    print("Current state: \n",
    "predictable combination of characters from letter range a-e in each bit of the guess")
    multi = 1
else:
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
    SERVER_IP = str(x)
except ValueError as e:
    print("please state valid server IP")
    sys.exit()
    pass #do nothing

message = sys.argv[1]
if message.isdigit() is False:
    print("Server carries a lsit of hashes to crack")
    print("please print which index in list of hashed passes u wish to crack")
    sys.exit()
# create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the socket to the server's address and port
server_address = (SERVER_IP, SERVER_PORT) #hard coded
client_socket.connect(server_address)

# send request to the server
# message = "please_work"
client_socket.sendall(message.encode())

# receive the server's response
data = client_socket.recv(1024)
print("received: ", data.decode())

to_crack = data.decode()


ans = "" #return iterated string to this 

if single == 1: #if single threaded chosen
    g = GuessGen.GuessGen()
    x = parseHash(to_crack)
    ans = g.crackCycle(to_crack) #bottleneck here most likely
elif multi == 1 :
    hg = HashGuesser.HashGuesser()
    hashed_lines = []
    hashed_lines.append(to_crack)
    numCrackers = []
    hg.generate_guessers(hashed_lines, numCrackers)
    t = len(os.sched_getaffinity(0)) #num of CPUs
    partitioned_letters = partition_letters(list(string.ascii_lowercase), t)
    initiate_multithreaded_cracking(partitioned_letters, numCrackers, t)
    ans = str(numCrackers)

client_socket.sendall(str(ans).encode())

print("reconnect to Server if more passwords left")

# close the socket
client_socket.close()


