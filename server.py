import socket
import os
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

print('Socket is listening..')
ServerSideSocket.listen()

def multi_threaded_client(connection):
    initial_send = { 'letter': raffled_letter, 'identifier': alphabet_list[ThreadCount - 1] }
    data = pickle.dumps(initial_send)
    connection.send(data)
    
    while True:
        data = connection.recv(4096)
        client_answer = pickle.loads(data)
        if not client_answer: 
            break
        print(client_answer)
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