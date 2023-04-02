import string
import threading
import time
import concurrent.futures
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import crypt

lock = threading.Lock()

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
        print(''.join(empty_list))
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

def start_cracking_given_letters(self,guessers, letters):
    letters_length = 1
    for hash_guesser in guessers:
        start = time.time()
        while hash_guesser.cracked_password is None:
            hash_guesser.crack_hash(list(letters), letters_length)
            letters_length += 1
        elapsed = time.time()
        hash_guesser.time_taken = elapsed - start
        letters_length = 1


def initiate_multithreaded_cracking(self,partitioned_letters, guessers, threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for letters in partitioned_letters:
            with lock:
                executor.submit(start_cracking_given_letters, guessers, letters)




def generate_guessers(self,hashed_lines, guessers):
    for hashed_line in hashed_lines:
        guessers.append(extract_etc_shadow(hashed_line))

def partition_letters(self,a, n):
        k, m = divmod(len(a), n)
        return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def show_results(self, guessers):
    print("----------- RESULTS -----------")

    for guess in guessers:
        print(guess)

def extract_etc_shadow(self,hashed_line):
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


def main():

    hashed_lines = ['sepehrman:$y$j9T$.Ciip2iHePTF7RvA1q3rX0$OeW1icDofEhPQhV4jPStlhsxPOmqmNcZlgaEfaXezE0:19381:0:99999:7:::\n', 'longpass:$1$Hc6V.QHW$NYVewhJpK/ejNYqbIuWqX/:19448:0:99999:7:::\n']
    # TODO: GET hashed lines here using Multicast Sockets (Maybe comma-separated?)

    guessers = []
    generate_guessers(hashed_lines, guessers)
    threads = 4
    print("Please wait. Cracking passwords")
    partitioned_letters = partition_letters(list(string.ascii_lowercase), threads)
    initiate_multithreaded_cracking(partitioned_letters, guessers, threads)
    show_results(guessers)


if __name__ == '__main__':
    main()