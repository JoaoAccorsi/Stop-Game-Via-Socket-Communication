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

print('Socket is listening..')
ServerSideSocket.listen()

def score():
    has_equal = 0
    number = 0

    print("client_answers_dict:\n", client_answers_dict)
    print("\n")

    # user_answer_dictionary['name'] = name

    # Fill the score_dictionary with the indentifiers 
    for i in range (len(client_answers_dict)):
        first_dict = client_answers_dict[i]
        aux = first_dict["identifier"]
        score_list.append({ 'identifier': aux, 'points': 0 })

    # Fill an array with all the names
    for i in range (len(client_answers_dict)):
        first_dict = client_answers_dict[i]
        name_value = first_dict["name"]
        array_name.append(name_value)

    # Judge the name
    for i in range (len(client_answers_dict)):
        first_dict = client_answers_dict[i]
        name_value = first_dict["name"]
        identifier_value = first_dict["identifier"]
        for j in range (len(array_name)):
            if (name_value == array_name[j]):
                has_equal +=1
        for k in range (len(score_list)):
            if ((score_list[k]['identifier']) == identifier_value):
                number = k
        if (has_equal == 1):
           score_list[number]['points'] += 10
           has_equal = 0
        else:
            score_list[number]['points'] += 5
            has_equal = 0

    print(score_list)

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

        print("\nNova Resposta:\n", client_answer)
        global first_client_to_send
        first_client_to_send = client_answer['identifier']
        client_answers_dict.append(client_answer)
        
        # Notify the other clients only once after the first one asked Stop
        if counter == 0:
            counter += 1
            # One client has already asked stop, got the awnser from the other(s)
            for i in range (len(identifiers_list)):
                # Find the identifiers of the clients which have not asked stop, and sent message "Forced Stop!" for them
                if first_client_to_send != identifiers_list[i]:       
                    new_connection = identifiers_connection_dict[identifiers_list[i]]
                    new_connection.send(encodedMessageForcedStop)

        flag += 1
        if (flag == 2):
            score()

    connection.close()

while True:
    client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    start_new_thread(multi_threaded_client, (client, ))
    print('Thread Number: ' + str(ThreadCount))

    # TRANCA!

    # receivedData = client.recv(1024)
    # if receivedData: 
    #     ServerSideSocket.close()
    #     break
    # print("Message from host %s: %s", address, receivedData.decode())
ServerSideSocket.close()
