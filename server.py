import socket
from _thread import *
import string
import random
import pickle
import struct

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

print('Socket is listening..')
ServerSideSocket.listen()

def score():

    print(client_answers_dict)
    print("\n")

    # Judge the Name
    for i in range (len(client_answers_dict)):
        first_dict = client_answers_dict[i]
        name_value = first_dict["name"]
        cep_value = first_dict["cep"]
        print("name: ", name_value)
        print("cep: ", cep_value)

def multi_threaded_client(connection):
    global counter

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
            counter = counter + 1
            # One client has already asked stop, got the awnser from the other(s)
            for i in range (len(identifiers_list)):
                # Find the identifiers of the clients which have not asked stop, and sent message "Forced Stop!" for them
                if first_client_to_send != identifiers_list[i]:         
                    new_connection = identifiers_connection_dict[identifiers_list[i]]
                    new_connection.send(encodedMessageForcedStop)
        print("\n")
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
