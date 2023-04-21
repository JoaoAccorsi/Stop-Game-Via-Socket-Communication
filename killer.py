import socket
import os
from _thread import *

ServerSideSocket = socket.socket()
ThreadCount = 0
ServerSideSocket.bind(('localhost', 6002))
ServerSideSocket.close()
