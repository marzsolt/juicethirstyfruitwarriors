import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()  # or 'IP address'
port = 12145                 # Random port number

s.connect((host, port))
print(s.recv(1024))
print(s.recv(1024))
s.close()                     # Close the socket when done