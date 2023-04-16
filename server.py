import socket
import string
import random

##-----------------------------
## Socket setup

    # Create a TCP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind (IP address, port)
socket.bind(("localhost", 2288))

    # Socket waiting for a connection in port 2244...
socket.listen()

    # Accept the connection for the listen above, and return the connection and address (IP address + port used to the connection)
connection, address = socket.accept()

##-----------------------------
## Game setup

alphabet_list = list(string.ascii_uppercase)
raffled_letter = alphabet_list[random.randrange(1, 26)]
encodedMessage = bytes(raffled_letter, 'utf-8')

cont = 0

##-----------------------------
## Game setup

while True:

        # Send the raffled letter to the client
    if (cont == 0):
        connection.send(encodedMessage)

        # Message received from the client
    receivedData = connection.recv(1024)
    
    if not receivedData:
        break
    print("Message from host %s: %s", address, receivedData.decode())

    cont = cont + 1
connection.close()
