import socket
import os
import tqdm

class Server:
    
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5001
        self.listening = 10
        self.buffer_size = 4096
    
    def server(self):
        BUFFER_SIZE = self.buffer_size
        SEPARATOR = "<SEPARATOR>"

        s = socket.socket()
        SERVER_HOST = self.host
        SERVER_PORT = self.port

        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(self.listening)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

        c, addr = s.accept()
        print(f"[+] {addr} is connected.")

        received = c.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)

        filename = os.path.basename(filename)
        filesize = int(filesize)

        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit='B', unit_scale=True, unit_divisor=1024)
        with open(filename, 'wb') as f:
            while True:
                bytes_read = c.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))
                
        c.close()
        s.close()


"Call server function of Server class as example"
server = Server()
server.server()