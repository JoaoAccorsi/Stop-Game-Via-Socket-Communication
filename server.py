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
encodedMessage = bytes(raffled_letter, 'utf-8')
encodedMessageForcedStop = bytes("Forced Stop!", 'utf-8')
first_client_to_send = ''
identifiers_list = []
identifiers_connection_dict = {}
counter = 0
client_answers_dict = []
score_list = []
flag = 0
array_name = []
identifiers_answer_array = []
client_answers_list = []
answers_keys = ['name', 'cep', 'food', 'object', 'team']
score_dictionary = {}

print('Socket is listening..')
ServerSideSocket.listen()

def score():
    has_equal = 0
    has_equal_answer = False
    number = 0

    print("client_answers_list:\n", client_answers_list)
    print("\n")

    # user_answer_dictionary['name'] = name

    # Fill the score_dictionary with the indentifiers 
    for i in range (len(client_answers_list)):
        first_dict = client_answers_list[i]
        identifier = first_dict["identifier"]
        score_list.append({ 'identifier': identifier, 'points': 0 })
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
    # # Fill an array with all the names
    # for i in range (len(client_answers_list)):
    #     first_dict = client_answers_list[i]
    #     name_value = first_dict["name"]
    #     array_name.append(name_value)

    # # Judge the name
    # for i in range (len(client_answers_list)):
    #     first_dict = client_answers_list[i]
    #     name_value = first_dict["name"]
    #     identifier_value = first_dict["identifier"]
    #     for j in range (len(array_name)):
    #         if (name_value == array_name[j]):
    #             has_equal +=1
    #     for k in range (len(score_list)):
    #         if ((score_list[k]['identifier']) == identifier_value):
    #             number = k
    #     if (has_equal == 1):
    #        score_list[number]['points'] += 10
    #        has_equal = 0
    #     else:
    #         score_list[number]['points'] += 5
    #         has_equal = 0

    print(score_list)
    print(score_dictionary, '<<<<<<<>>>>>>>')
    print("\n")

def multi_threaded_client(connection):
    global counter,flag

    client_identifier = alphabet_list[ThreadCount - 1]
    identifiers_list.append(client_identifier)
    identifiers_connection_dict[client_identifier] = connection

    initial_send = { 'letter': raffled_letter, 'identifier': client_identifier }
    data = pickle.dumps(initial_send)
    connection.send(data)
    
    while True:
        data = connection.recv(4096)
        client_answer = pickle.loads(data)
        
        if not client_answer: 
            break

        # print("\nNova Resposta:\n", client_answer)
        global first_client_to_send
        first_client_to_send = client_answer['identifier']
        client_answers_list.append(client_answer)        
        # Notify the other clients only once after the first one asked Stop
        if counter == 0:
            counter += 1
            # One client has already asked stop, got the awnser from the other(s)
            for identifier in identifiers_list:
                # Find the identifiers of the clients which have not asked stop, and sent message "Forced Stop!" for them
                if first_client_to_send == identifier:continue       
                new_connection = identifiers_connection_dict[identifier]
                new_connection.send(encodedMessageForcedStop)

        # flag += 1
        # if (flag == 2):
        #     score()

    connection.close()

def get_and_send_results():
    global client_answers_list
    global ThreadCount

    # Wait for all clients to send their answers
    while ThreadCount != len(client_answers_list): continue
    print("We have all answers!")
    score()
    # print(identifiers_answer_array)
    # for identifier in identifiers_list:
    #     identifier_connection = identifiers_connection_dict[identifier]
    #     identifier_connection.send(bytes("your points!", 'utf-8'))
    #     print("sent!") 


while True:
    client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    start_new_thread(multi_threaded_client, (client, ))
    print('Thread Number: ' + str(ThreadCount))
    
    if ThreadCount == 1:
        start_new_thread(get_and_send_results, ())
    
    # TRANCA!

    # receivedData = client.recv(1024)
    # if receivedData: 
    #     ServerSideSocket.close()
    #     break
    # print("Message from host %s: %s", address, receivedData.decode())
