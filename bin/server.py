import socket, subprocess, ssl

import ast, os, sys, base64

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('gen/server.pem')

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ensure that you can restart your server quickly when it terminates
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock = ssl.wrap_socket(
    sock, server_side=True, certfile="gen/server.pem"
)

# Set the client socket's TCP "well-known port" number
well_known_port = 1443
sock.bind(('', well_known_port))

# Set the number of clients waiting for connection that can be queued
sock.listen(3)

# loop waiting for connections (terminate with Ctrl-C)
pieces = []

print("Waiting for clients to send pieces...")

try:
    while 1:
        newSocket, address = sock.accept(  )
        newSocket.send("Enter a piece:\n".encode())
        receivedData = newSocket.recv(1024)
        pieces.append(receivedData)
        newSocket.send("Thanks!!\n".encode())
        newSocket.close(  )
        print("Received %s of 3 pieces!" % len(pieces))
        if len(pieces) >= 3: break
finally:
    sock.close(  )
    process = subprocess.Popen(['ssss-combine', '-x', '-t', '3', '-Q'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for piece in pieces:
        process.stdin.write(piece)
    process.stdin.close()
    output = process.stderr.read()
    output = output.decode("utf-8").replace("\n", "")

secret = base64.b64decode(sys.argv[1])

with open('gen/masterkey.pem') as privatefile:
	privateKey = load_pem_private_key(privatefile.read().encode(), str.encode(output))

decMessage = privateKey.decrypt(secret, padding.PKCS1v15())

print("\n\nSecret:\n\n" + decMessage.decode("utf-8"))