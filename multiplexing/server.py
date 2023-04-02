import select
import socket
import sys
import GuessGen

SERVER_PORT = 5000
unlock_pw = "please_work"
#default hashed pass to crack. yescrypt for-> 2!
def_toCrack = "$y$j9T$oHjB961YNYYZaS/B9V5sr1$eqVAPSL4NpprMtfP9ie6jayp.rdiGsdFQPa/KRVOxm7" 
#hash for @1
def_toCrack2 = "$y$j9T$i8yp74CnZmCPRJVoEMqzq.$8qhOee2ONuRaDFw1Ol5YCYg5JzJGUStUkLV7gqO9pp6"
# hash for f3
def_toCrack3 = "$y$j9T$oH7nWb5ua.cMKZ/UbFzgO1$1.SCQJJKyGBoLdSRqbJuERDvyOaVvIA3qHy6F9UeRB5"
default_mode = 0 # use a preset password for testing
full_mode = 0 # server will read its /etc/shadow if 1 
cracked_pw = ""

if sys.argv[1] is None:
    printUsage()

if sys.argv[1] == "-f":
    full_mode = 1
elif sys.argv[1] == "-d":
    default_mode= 1
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


numConnections = int(sys.argv[2])
if numConnections > 10 :
    print("maximum 10 connections allowed.\nSet to 5 as default")
    numConnections = 5
    pass

users = [] #List of users to crack
if full_mode == 1:
    try:
        tag_found = sys.argv.index("-u")
        list_users = sys.argv[(tag_found+1):len(sys.argv)] #extract users as list
        for u in list_users:
            users.append(u) #add user
    except ValueError as e:
        print("must use -u to list users")
        sys.exit()
# numUsers = 1
# while(numUsers < len(sys.argv)):
#     users.append(sys.argv[numUsers])
#     numUsers +=1
#     #List of users added

hashed_passes = []

if full_mode == 1:
    for u in users:
        #Module that will search for username in command line
        with open('/etc/shadow') as f:
            line = f.read()
            print(line)
            uName_Index = line.find(u)
            if uName_Index != -1: #if username found
                passIndexFirst = len(u) + 1
                chop = line[uName_Index+(passIndexFirst):] #starting from first index where username found + add up to index of when pass starts 
                colonAfterPass = chop.find(":") #find index of first occurrence of colon
                hashed = chop[0:colonAfterPass] #excluded colon index
                print("extracted hash:",end="")
                print(hashed)
                userInfo = (u,hashed) 
                hashed_passes.append(userInfo)
        #end of file context
    #end of for loop
    if len(hashed_passes) == 0:
        print("no hash pass found")
        sys.exit()
    else:
        print("following hashed passwords found")
        for h in hashed_passes:
            print(h[0], ": ", h[1])

elif default_mode == 1:
    hashed_passes.append(def_toCrack)
    hashed_passes.append(def_toCrack2)
    hashed_passes.append(def_toCrack3)
    defaultMultiplex()
    print(cracked_pw)
    sys.exit()


#solved_passes = []
# to_crack = hashed_passes[0] #first password found for now

if full_mode == 1:
    for crackThis in hashed_passes:
        x = mainMultiplex(crackThis[1])
        print("pass for ", hashed_passes[0], " is ", x)
elif default_mode == 1 :
    for crackThis in hashed_passes:
        x = defaultMultiplex(crackThis)
        print("pass is: ", x)


#multiplex function for file mode
def mainMultiplex(user_pw_hash):
    
    # create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #socket level, REUSEADDR option, set to nonzero. helps us have 2 sockets at same port
    #doc: https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html#Socket_002dLevel-Options
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind the socket to a specific address and port
    server_address = ('0.0.0.0', SERVER_PORT)
    server_socket.bind(server_address)

    # listen for incoming connections
    server_socket.listen(numConnections)

    # create a list of sockets to monitor for incoming data
    inputs = [server_socket]
    keep = 1
    while keep == 1:
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
                    # echo the default hash back to the client
                    sock.sendall(user_pw_hash.encode())
                else:
                    if data.decode() == "NO_PW_FOUND" :
                        print("client could not find password")
                        sock.close()
                        inputs.remove(sock)
                    else:
                        print("response from a client")
                        print("pass is ", data.decode())
                        pw = data.decode()
                        keep = 0
                        sock.close()
                        inputs.remove(sock)
                        # close the socket
                        #sock.close()
                        #inputs.remove(sock)
    #end of while
    return pw


#multiplex function for default mode. takes a single hash pass
def defaultMultiplex(hash_pw):
    
    # create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #socket level, REUSEADDR option, set to nonzero. helps us have 2 sockets at same port
    #doc: https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html#Socket_002dLevel-Options
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind the socket to a specific address and port
    server_address = ('0.0.0.0', SERVER_PORT)
    server_socket.bind(server_address)

    # listen for incoming connections
    server_socket.listen(numConnections)

    # create a list of sockets to monitor for incoming data
    inputs = [server_socket]
    keep = 1
    while keep == 1:
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
                    # echo the default hash back to the client
                    sock.sendall(hash_pw.encode())
                else:
                    if data.decode() == "NO_PW_FOUND" :
                        print("client could not find password")
                        sock.close()
                        inputs.remove(sock)
                    else:
                        print("response from a client")
                        print("pass is: ", data.decode())
                        pw = data.decode()
                        keep = 0 
                        sock.close()
                        inputs.remove(sock) 
                        # close the socket
                        #sock.close()
                        #inputs.remove(sock)
            #end of going through any sockets where we read data from
        #end of while
    return pw

def printUsage():
    print("usage:")
    print("first argument is either: \n\t\'-d\' for default mode or \n\t\'-f\' for file mode ")
    print("default mode utilizes a preset hash for testing. Usage:")
    print("sudo python3 server.py -d")
    print("\'-f\' file mode usage:")
    print("sudo python3 server.py -f [number of machines] -u <user1> <user2> <user(n)...>")
    print("\'-u\'\tList all username(s) whose password(s) desired to crack one by one, separated by space")
    print("    \tstate list of users always at the end")
    print("(optional) \'-p\' [number] sets a server port. default is 5000. Can be used in both modes")