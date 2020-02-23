import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server
host = socket.gethostname()  # or 'IP address'
port = 12145                 # Random port number
s.bind((host, port))

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from')
   print(addr)
   c.send(b'Thank you for connecting')
   c.close()                # Close the connection
