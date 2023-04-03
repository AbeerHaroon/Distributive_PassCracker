import argparse
import multiprocessing
import string
import threading
import time
import concurrent.futures
import warnings
import socket

from client_request import ClientRequest



with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import crypt

lock = threading.Lock()

DEFAULT_PORT = 5000



def define_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out', help='The IP of the server in which we are connecting to.', required=True)
    parser.add_argument('-p', '--port', help='The Port number of the server we are connecting to. Defaults to 5000', default=DEFAULT_PORT)
    parser.add_argument("-t", "--threads", help=f"The number of threads we would like to run the program on. "
                                                "Defaults to the current machine's number of CPU Cores", default=multiprocessing.cpu_count())
    
    
    request = ClientRequest()
    args = parser.parse_args()
    request.ip = args.out
    request.port = int(args.port)
    request.threads = int(args.threads)

    return request


class HashGuesser:

    def __init__(self):
        self.username = None
        self.hashed = None
        self.id = None
        self.salt = None
        self.last_updated = None
        self.hashed_password = None
        self.cracked_password = None
        self.hashing_type = None
        self.tries = 0
        self.time_taken = None

    def __str__(self):
        return f'"{self.username}" is using the "{self.hashing_type}" hashing algorithm.\n' \
               f'Cracked Password: "{self.cracked_password}"\n' \
               f'Number of trials: {self.tries}\n' \
               f'Time taken: {self.time_taken:.6f} (seconds)\n'

    def crack_hash(self, char_list, n, empty_list=[]):
        guess = crypt.crypt(''.join(empty_list), self.hashed_password)
        self.tries += 1
        if guess == self.hashed_password:
            self.cracked_password = ''.join(empty_list)

        if len(empty_list) == n:
            pass
        else:
            for c in char_list:
                if self.cracked_password is not None:
                    return True
                self.crack_hash(char_list, n, empty_list + [c])

    def identify_hash(self):
        self.hashing_type = 'N/A'
        if self.hashed_password.startswith('$1$'):
            self.hashing_type = 'MD5'
        elif self.hashed_password.startswith('$2a$'):
            self.hashing_type = 'Blowfish'
        elif self.hashed_password.startswith('$2y$'):
            self.hashing_type = 'Blowfish'
        elif self.hashed_password.startswith('$5$'):
            self.hashing_type = 'SHA-256'
        elif self.hashed_password.startswith('$6$'):
            self.hashing_type = 'SHA-512'
        elif self.hashed_password.startswith('$y$'):
            self.hashing_type = 'yescrypt'

def start_cracking_given_letters(guessers, letters):
    letters_length = 1
    for hash_guesser in guessers:
        start = time.time()
        while hash_guesser.cracked_password is None:
            hash_guesser.crack_hash(list(letters), letters_length)
            letters_length += 1
        elapsed = time.time()
        hash_guesser.time_taken = elapsed - start
        letters_length = 1


def initiate_multithreaded_cracking(partitioned_letters, guessers, threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for letters in partitioned_letters:
            with lock:
                executor.submit(start_cracking_given_letters, guessers, letters)



def generate_guessers(hashed_lines, guessers):
    for hashed_line in hashed_lines:
        guessers.append(extract_etc_shadow(hashed_line))

def partition_letters(a, n):
        k, m = divmod(len(a), n)
        return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def show_results(guessers, threads):
    result =f"\n----------- RESULTS w/{threads} threads -----------\n"
    for guess in guessers:
        result += f'{guess}\n'
    return result

def extract_etc_shadow(hashed_line):
    info_array = hashed_line.split(":")
    hash_details = info_array[1][1:].split('$')

    hash_guess = HashGuesser()
    hash_guess.username = info_array[0]
    hash_guess.id = hash_details[0]

    hash_guess.salt = hash_details[1]
    hash_guess.hashed = hash_details[2]
    hash_guess.last_updated = info_array[2]
    hash_guess.hashed_password = info_array[1]
    hash_guess.identify_hash()
    return hash_guess


import socket



def make_request_to_server(request):

    try:
        SERVER_ADDR = request.ip
        SERVER_PORT = request.port
        THREADS = request.threads

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_ADDR, SERVER_PORT))

        # Receive and print the welcome message from the server
        hashed_lines = client_socket.recv(1024).decode()
        hashed_lines = hashed_lines.split(',')

        guessers = []
        generate_guessers(hashed_lines, guessers)

        print(f"Please wait. Cracking passwords using '{THREADS}' Threads...\n")

        if THREADS == 1:
            start_cracking_given_letters(guessers, string.printable)
        elif THREADS > 1:
            partitioned_letters = partition_letters(list(string.ascii_lowercase), THREADS)
            initiate_multithreaded_cracking(partitioned_letters, guessers, THREADS)

        results = show_results(guessers, THREADS)
        print(results)
        client_socket.send(results.encode())

        # Close the socket
        client_socket.close()
    except Exception as e:
        print(f'{e}')
    finally:
        client_socket.close()




def main():
    request = define_arguments()
    make_request_to_server(request)





if __name__ == '__main__':
    main()