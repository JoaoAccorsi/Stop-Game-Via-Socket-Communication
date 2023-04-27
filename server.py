import socket
from _thread import *
import string
import random
import pickle

ServerSideSocket = socket.socket()
ThreadCount = 0
ServerSideSocket.bind(('localhost', 6002))

alphabet_list = list(string.ascii_uppercase)
raffled_letter = alphabet_list[random.randrange(1, 26)]
encoded_send_anwser_event = bytes("send_answers", 'utf-8')
identifiers_list = []
identifiers_connection_dict = {}
have_someone_called_stop = False
client_answers_list = []
answers_keys = ['name', 'cep', 'food', 'object', 'team']
score_dictionary = {}
first_client_to_finish = ''

print('Socket is listening..' + "\n")
ServerSideSocket.listen()

def result():
    print("\n-----\nFinal Result\n-----")
    print("\nScore: ", score_dictionary)
    print("\n\n")

def score():
    has_equal_answer = False

    # Fill the score_dictionary with the indentifiers 
    for i in range (len(client_answers_list)):
        first_dict = client_answers_list[i]
        identifier = first_dict["identifier"]
        score_dictionary[identifier] = 0
    
    for key in answers_keys:
        for client_answer in client_answers_list:
            client_identifier = client_answer["identifier"]
            key_answer = client_answer[key].lower()
            if key_answer == "" or key_answer[0] != raffled_letter.lower():
                continue
            for client_to_compare_answer in client_answers_list:
                if client_to_compare_answer["identifier"] == client_answer["identifier"]:
                    continue
                client_to_compare_key_answer = client_to_compare_answer[key].lower()
                if client_to_compare_key_answer == key_answer:
                    has_equal_answer = True
                    break
            if has_equal_answer:
                score_dictionary[client_identifier] += 5
                has_equal_answer = False
            else:
                score_dictionary[client_identifier] += 10
                has_equal_answer = False

    result()

def stop_event_control(data):
    finish_first_identifier = data['identifier']
    for identifier in identifiers_list:
        new_connection = identifiers_connection_dict[identifier]
        send_answers_dict = { 'event': 'send_answers', "finish_first_identifier": finish_first_identifier }
        new_connection.send(pickle.dumps(send_answers_dict))
    return

def answers_control(client_answer):
    client_answers_list.append(client_answer) 

def multi_threaded_client(connection):
    client_identifier = alphabet_list[ThreadCount - 1]
    identifiers_list.append(client_identifier)
    identifiers_connection_dict[client_identifier] = connection

    initial_send = { 'letter': raffled_letter, 'identifier': client_identifier }
    data = pickle.dumps(initial_send)
    connection.send(data)
    while True:
        data_received = connection.recv(4096)
        if not data_received: 
            break

        data = pickle.loads(data_received)
        data_event = data['event']  
        if data_event.decode() == "stop": 
            stop_event_control(data)
        else:
            answers_control(data) 

def get_and_send_results():
    global client_answers_list
    global ThreadCount

    # Wait for all clients to send their answers
    while ThreadCount != len(client_answers_list): continue
    score()
    # get who is the winner!
    
    winner_arr = []
    winner_identifier = max(score_dictionary, key=score_dictionary.get)
    winner_arr.append(winner_identifier)
    winner_number_of_points = score_dictionary[winner_identifier]
    # checking if there is any other identifier with the same amount of points
    for key in score_dictionary:
        if score_dictionary[key] == winner_number_of_points and key != winner_identifier:
            winner_arr.append(key)

    for identifier in identifiers_list:
        results_dict = {
            'event': 'results',
            'number_of_winners': len(winner_arr),
            'current_identifier_points': score_dictionary[identifier], 
            'winner_identifier': winner_arr, 
            "winner_points": score_dictionary[winner_identifier]
        }
        identifier_connection = identifiers_connection_dict[identifier]
        results_dict_data = pickle.dumps(results_dict)
        identifier_connection.send(results_dict_data)

while True:
    client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    start_new_thread(multi_threaded_client, (client, ))
    print('Thread Number: ' + str(ThreadCount) + "\n")
    
    if ThreadCount == 1:
        start_new_thread(get_and_send_results, ())
