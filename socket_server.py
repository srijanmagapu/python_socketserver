import socket


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 8000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print ('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        data = connection.recv(16)
        print ('received "%s"' % data)
        if data:
            print ('sending data back to the client')
            connection.send('HTTP/1.0 200 OK\n')
            connection.send('Content-Type: text/html\n')
            connection.send('\n') # header and body should be separated by additional newline
            connection.send("""<html>
                        <body>
                        <h1>Hello World</h1> this is my server!
                        </body>
                        </html>
                        """) # Use triple-quote string.

        else:
            print ('no more data from', client_address)
            break
            
    finally:
    # Clean up the connection
            connection.close()
