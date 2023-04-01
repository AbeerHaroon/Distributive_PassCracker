import argparse
import string
import threading
import time
import concurrent.futures
import warnings
import multiprocessing
from request import Request
from hash_guesser import HashGuesser

lock = threading.Lock()


def define_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='The shadow file we want to crack the password of.')
    parser.add_argument('users', nargs='*', help="Argument with no flag that is a list of usernames")
    parser.add_argument("-t", "--threads", help=f"The number of threads we would like to run the program on. "
                                                "Defaults to the current machine's number of CPU Cores",
                        default=multiprocessing.cpu_count())
    parser.add_argument('--time', help='The shadow file we want to crack the password of.')
    parser.add_argument('--trials', help='The shadow file we want to crack the password of.')


    request = Request()
    args = parser.parse_args()
    request.file = args.file
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

def main():
    request = define_arguments()
    hashed_lines = []
    guessers = []

    find_lines(request, hashed_lines)
    print("Cracking Passwords. Awaiting on other computers responses.")
    print('hashed LINES ', hashed_lines)
    # TODO: Send the lines to the receiver (hash_guesser)
    

if __name__ == '__main__':
    main()



