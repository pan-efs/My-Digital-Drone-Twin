import socket
import os
import tqdm

class Client:
    def client(self, filename: str):
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096

        s = socket.socket()
        host = "127.0.0.1"
        port = 5001

        "Take one file as example from logs directory"

        filesize = os.path.getsize(filename)

        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
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