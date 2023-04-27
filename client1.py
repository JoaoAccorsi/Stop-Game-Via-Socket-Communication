import socket  
import pickle
from sendAnswersToServerThread import SendAnswersToServerThread
from keyboardEventsThread import KeyboardEventsThread
 
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Create a TCP socket
socket.connect(("localhost", 6002))                              # Connect to the socket created in the server

user_answer_dictionary = {
  'name': " ",
  'cep': " ",
  'food': " ",
  'object': " ",
  'team': " "
}
have_send_answer = False
encoded_stop_event = bytes("stop", 'utf-8')
encoded_send_answer_event = bytes("send_answers", 'utf-8')

def send_users_answers():
  global have_send_answer

  user_answer_dictionary['event'] = encoded_send_answer_event
  data = pickle.dumps(user_answer_dictionary)
  socket.send(data)
  have_send_answer = True
  return

def send_stop_call(identifier):
  stop_call = { 'identifier': identifier, "event": encoded_stop_event }
  data = pickle.dumps(stop_call)
  socket.send(data)
  return 

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
  print("Seu identificador é a letra: " + identifier)
  print("Letra sorteada: " + letter)
  
  listen_to_keyboard_thread = KeyboardEventsThread(socket, user_answer_dictionary, identifier, send_stop_call)
  listen_to_keyboard_thread.start()

  send_answers_to_server_thread = SendAnswersToServerThread(socket, send_users_answers, listen_to_keyboard_thread, identifier)
  send_answers_to_server_thread.start()

  while have_send_answer == False: continue
  send_answers_to_server_thread.stop()
  listen_to_keyboard_thread.join()
  send_answers_to_server_thread.join()

  results = socket.recv(4096)
  results_dict = pickle.loads(results)

  client_points = results_dict['current_identifier_points']
  if results_dict['winner_identifier'] == identifier:
    print("\nVocê obteve " + str(client_points) + " pontos e foi o vencedor!\n")
  else:
    print("Você obteve " + str(client_points) + " pontos e não foi o vencedor!")
    print("Venceu o jogador " + results_dict['winner_identifier'] + " com " + str(results_dict['winner_points']) + " pontos.\n")
  socket.close()
  break
