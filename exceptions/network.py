#                          #
#----------Client----------#
#                          #
class ConnectToServerError(Exception):
    def __init__(self, server_host, server_port, message = 'Cannot connect to:'):
        self.message = message
        self.server_host = server_host
        self.server_port = server_port
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message} {self.server_host}:{self.server_port}'

class SendingFileError(Exception):
    def __init__(self, filename, filesize = 0, message = 'Sending has been failed:'):
        self.message = message
        self.filename = filename
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message} {self.filename}'

#                          #
#----------Server----------#
#                          #
class BindToClientError(Exception):
    def __init__(self, server_host, server_port, message = 'Cannot bind to:'):
        self.message = message
        self.server_host = server_host
        self.server_port = server_port
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message} {self.server_host}:{self.server_port}'
    
class ListeningToClientError(Exception):
    def __init__(self, listening_time = 000, message = 'Listening time has passed:'):
        self.message = message
        self.listening_time = listening_time
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message} {self.listening_time}'

class AcceptToClientError(Exception):
    def __init__(self, message = 'Connection has not been accepted:'):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

class ReceivingFileError(Exception):
    def __init__(self, message = 'Receiving file was unsuccessful.'):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'
