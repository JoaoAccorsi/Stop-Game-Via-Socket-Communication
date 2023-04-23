import socket  
import pickle
import threading
import struct

    # Create a TCP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect to the socket created in the server
socket.connect(("localhost", 6002))

user_answer_dictionary = {}
have_send_answer = False


def send_users_answers():
  data = pickle.dumps(user_answer_dictionary)
  socket.send(data)

def listen_to_keyboard_inputs():
  name = input("Nome: ")
  user_answer_dictionary['name'] = name

  cep = input("CEP: ")
  user_answer_dictionary['cep'] = cep

  food = input("Comida: ")
  user_answer_dictionary['food'] = food

  object = input("Objeto: ")
  user_answer_dictionary['object'] = object

  team = input("Time de futebol: ")
  user_answer_dictionary['team'] = team

  send_users_answers()
  global have_send_answer
  have_send_answer = True

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
  
  user_answer_dictionary['identifier'] = identifier
  print("Letra sorteada: " + letter)
  thread = threading.Thread(target = listen_to_keyboard_inputs)
  thread.start()

  if have_send_answer == False:
    packed_boolean = socket.recv(1)
    has_another_client_finished = struct.unpack('?', packed_boolean)[0]
    if has_another_client_finished == True:
      thread.join(timeout = 0.1)
      print("O outro cliente terminou")
      send_users_answers()

  print("hello guys")

  ## quem ganhou?? etc

