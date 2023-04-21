import socket  
import pickle
    # Create a TCP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect to the socket created in the server
socket.connect(("localhost", 6002))

cont = 0

  # Send the data from the client to the server
while True:
    
  if (cont == 0):  
    data = socket.recv(4096)
    initial_receive = pickle.loads(data)  
  cont = cont + 1

  if not initial_receive:
    break
    
  identifier = initial_receive['identifier']
  letter = initial_receive['letter']
  print(initial_receive)
  
  print("Letra sorteada: " + letter)
  name = input("Nome: ")
  cep = input("CEP: ")
  food = input("Comida: ")
  object = input("Objeto: ")
  team = input("Time de futebol: ")

  answersDictionary = { 'identifier': identifier, 'name': name, 'cep': cep, 'food': food, 'object': object, 'team': team }
  data = pickle.dumps(answersDictionary)
  socket.send(data)
  ## quem ganhou?? etc
