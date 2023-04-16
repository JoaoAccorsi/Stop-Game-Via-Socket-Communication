import socket  

    # Create a TCP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect to the socket created in the server
socket.connect(("localhost", 2288))

cont = 0

  # Send the data from the client to the server
while True:
    
  if (cont == 0):
    raffled_letter = socket.recv(1024).decode()
    if not raffled_letter:
        break
    else:
        print("The Raffled Letter is:", raffled_letter)

  message = input("Type your message: ")
  socket.send(message.encode())

  cont = cont + 1
