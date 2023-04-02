import argparse
import string
import threading
import time
import concurrent.futures
import warnings
import multiprocessing
from request import Request
from hash_guesser import HashGuesser
import socket
import select

DEFAULT_PORT = 5000
DEFAULT_IP = socket.gethostbyname(socket.gethostname())

def define_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='The shadow file we want to crack the password of.')
    parser.add_argument('users', nargs='*', help="Argument with no flag that is a list of usernames")
    parser.add_argument('--time', help='The shadow file we want to crack the password of.')
    parser.add_argument('--trials', help='The shadow file we want to crack the password of.')
    parser.add_argument('-i', '--input', help='The IP Address in which we want to start our server. Defaults to IP of current machine', default=DEFAULT_IP)
    parser.add_argument('-p', '--port', help='The Port number in which we are stating our server on. Defaults to 5000', default=DEFAULT_PORT)
    parser.add_argument("-t", "--threads", help=f"The number of threads we would like to run the program on. "
                                                "Defaults to the current machine's number of CPU Cores", default=multiprocessing.cpu_count())


    request = Request()
    args = parser.parse_args()
    request.file = args.file
    request.port = args.port
    request.ip = args.input
    request.users = args.users
    request.threads = int(args.threads)
    request.time = args.time
    request.trials = args.trials

    errors = []
    
    if request.file is None:
        errors.append("Must include a file with the following argument -f/--file")

    if len(request.users) == 0 or request.users is None:
        errors.append("Must include username(s)")

    if request.file is None:
        errors.append("Must include a shadow fie to look at the hash")

    if len(errors) > 0:
        display_errors(errors)

    return request


def display_errors(errors):
    for error in errors:
        print(f'-\t{error}')
    quit()



def find_lines_from_user(req: Request, username):
    with open(req.file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(username):
                return line
    print(f"*** Warning: '{username}' is not associated with this file. Cannot crack password. ***")


def find_lines(request, hashed_lines):
    for user in request.users:
        found = find_lines_from_user(request, user)
        if found:
            hashed_lines.append(found)
    if len(hashed_lines) == 0:
        print("!!! Error: None of the usernames provided are available within the shadow file. Please check the "
              "usernames. !!!")
        quit()



def handle_multiplexing(request: Request, hashed_lines):

    # Define server address and port
    SERVER_ADDR = request.ip
    SERVER_PORT = request.port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_ADDR, SERVER_PORT))

    server_socket.listen(999)
    sockets_list = [server_socket]

    print(f'Server is listening on {SERVER_ADDR}:{SERVER_PORT}')

    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])
        for sock in read_sockets:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                print(f'\nNew connection from {client_address}')

                msg = ','.join(hashed_lines)
                print(f'Cracking the following hashes:\n{msg}')
                client_socket.send(msg.encode())
                sockets_list.append(client_socket)
            else:
                # If the socket is a client socket, receive and print any incoming data
                data = sock.recv(1024).decode().strip()
                if data:
                    print(f'Received data from {sock.getpeername()}: \n\n{data}')
                else:
                    # If the socket is closed, remove it from the list of sockets to monitor
                    sockets_list.remove(sock)
                    print(f'Connection closed by {sock.getpeername()}')




def main():
    request = define_arguments()
    hashed_lines = []

    find_lines(request, hashed_lines)
    print("Cracking Passwords. Awaiting other computers to finish cracking...\n")
    handle_multiplexing(request, hashed_lines)
    

if __name__ == '__main__':
    main()


