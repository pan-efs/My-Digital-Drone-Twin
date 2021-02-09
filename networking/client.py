import socket
import os
import tqdm
import sys

class Client:
    
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5001
        self.buffer_size = 4096
    
    def client(self, filename: str):
        BUFFER_SIZE = self.buffer_size
        SEPARATOR = "<SEPARATOR>"

        s = socket.socket()
        SERVER_HOST = self.host
        SERVER_PORT = self.port

        "Take one file as example from logs directory"

        filesize = os.path.getsize(filename)

        print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
        
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
        except OSError:
            print('Error connecting to server.')
            sys.exit(1)
        
        print("[+] Connected.")

        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit='B', unit_scale=True, unit_divisor=1024)
        with open(filename, 'rb') as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
                
        s.close()
        
"Call client function of Client class as example"
client = Client()

client.client('C:/Users/user/Desktop/KTH/Master Thesis/Logs cpp/position_X.txt')