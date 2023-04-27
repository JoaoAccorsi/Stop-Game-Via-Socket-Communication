import socket  
import pickle
import threading

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
socket.connect(("localhost", 6002))                         # Connect to the socket created in the server

user_answer_dictionary = {}
have_send_answer = False
identifiers_thread_dict = {}
identifiers_list = []

def send_users_answers():

  # Ensure that no empty values are sent for the server
  if not "name" in user_answer_dictionary:
    user_answer_dictionary['name'] = " "

  if not "cep" in user_answer_dictionary:
    user_answer_dictionary['cep'] = " "
    
  if not "food" in user_answer_dictionary:
    user_answer_dictionary['food'] = " "

  if not "object" in user_answer_dictionary:
    user_answer_dictionary['object'] = " "

  if not "team" in user_answer_dictionary:
    user_answer_dictionary['team'] = " "

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

counter = 0

  # Send the data from the client to the server
while True:
    # Receive the identifier and the raffled letter initially sent
  if (counter == 0):  
    data = socket.recv(4096)
    initial_receive = pickle.loads(data)  
  counter = counter + 1

  if not initial_receive:
    break
    
  identifier = initial_receive['identifier']
  letter = initial_receive['letter']
  
  user_answer_dictionary['identifier'] = identifier
  print("Letra sorteada: " + letter)

  thread = threading.Thread(target = listen_to_keyboard_inputs)
  thread.start()

  identifiers_list.append(identifier)
  identifiers_thread_dict[identifier] = thread
  
    # The other client has asked Stop! Force this client to sent their currently awnsers
  if have_send_answer == False:
    new_received_data = socket.recv(1024)
    if (new_received_data.decode() == "Forced Stop!"):
      print("\nO outro cliente terminou")
      thread = identifiers_thread_dict[identifier]
      thread.join(timeout = 0.1)
      initial_receive = None
      send_users_answers()
      initial_receive = None

  print("hello guys")
