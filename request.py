class Request():

    def __init__(self):
        self.users = None
        self.file = None
        self.threads = None
        self.ip = None
        self.port = None

    def __str__(self):
        return f'(users: {self.users}, file: {self.file}, threads: {self.threads})'

    def __repr__(self):
        return f'(users: {self.users}, file: {self.file}, threads: {self.threads})'