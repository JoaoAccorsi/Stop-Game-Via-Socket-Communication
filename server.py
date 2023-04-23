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
first_client_to_send = ''
identifiers_list = []
identifiers_connection_dict = {}

print('Socket is listening..')
ServerSideSocket.listen()

def multi_threaded_client(connection):
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
        print(client_answer)
        global first_client_to_send
        first_client_to_send = client_answer['identifier']

        # for identifier in identifiers_list:
        #     if identifier == first_client_to_send: continue
        #     connection = identifiers_connection_dict[identifier]
        #     packed_value = struct.pack('?', True)            
        #     connection.send(packed_value)
        #     data = connection.recv(4096)
        #     other_answer = pickle.loads(data)
        #     print(other_answer, '<<<<other answer')
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