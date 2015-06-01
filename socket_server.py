import socket
import os

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
        data = connection.recv(1024)
        #GET={i.split("=")[0]:i.split("=")[1] for i in data.split("\n")[0].split(" ")[1][2:].split("&")}
        print data
        #   print connection.getpeername()
        
        print ('received "%s"' % data)
        if data:
            print ('sending data back to the client')
            connection.send('HTTP/1.0 200 OK\n')
            connection.send('Content-Type: text/html\n')
            connection.send('\n') # header and body should be separated by additional newline
            connection.send("""<html>
                        <body>
                        <h1>Hello World</h1>""")
            connection.send("<ul>");
            link = data.split(" ")[1];
            print link
            if "/" != link:
                if "favicon.ico" not in data:
                    path = os.path.join(os.getcwd(), link)
                    print "**************************"+path
            else:
                path = os.getcwd();
                print "-------------------"+path
            for files in os.listdir(path):
                print files
                fname = os.path.join(path,files)
                if os.path.isdir(fname):
                    fileName = """<li><a href="{0}" >{0}</a></li>"""
                else:
                    fileName = """<li>{0}</li>"""
                connection.send(fileName.format(fname));
            connection.send("""</ul>
                        </body>
                        </html>
                        """) # Use triple-quote string.
        else:
            print("NO Data");
            connection.close();
    finally:
    # Clean up the connection
            connection.close()
