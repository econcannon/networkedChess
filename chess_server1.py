# This file is intended to initialize the server of the game
#Maintain main board and board list
#CheckMate checking
#In check Checking
#	Sends a notification back to reverse the move locally and make another move.

from mvc.Controller.server_game_controller1 import ServerGameController
import socket
import time
import atexit
import subprocess


class Chess_Server():

    def __init__(self) -> None:

        # Initialize variables
        HOST = ''
        PORT = 12004
        IDENTIFIER = (HOST, PORT)

        subprocess.call([r'C:\Users\ericd\OneDrive\Desktop\NEU\!Coding\2140\networkedChess\open_port.bat'])

        # Create and bind Server Soceket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Host socket created...')
            
        self.server_socket.bind(IDENTIFIER)
        self.connection_socket = [0 for i in range(2)]
        self.client_address = [0 for i in range(2)]

        atexit.register(self.disconnect)

        # Change default timeout
        self.server_socket.settimeout(60)

        print('Server listening for connection...')
        self.server_socket.listen(2)
        num_connections = 0

        message = 'You are connected'.encode()
        while num_connections < 2:
            
            self.connection_socket[num_connections], self.client_address[num_connections] = self.server_socket.accept()
            self.connection_socket[num_connections].send(message)
            print('Connection created at', self.client_address[num_connections])
            num_connections += 1
                        
        # First client to join chooses player color
        while True:
            message = ('Choose your color\n' + 'Enter \'w\' or \'b\'').encode()
            self.connection_socket[0].send(message)

            answer = self.connection_socket[0].recv(1024).decode()
            print(f'Server received {answer} from client 1')

            if (answer == 'w'):
                # For game controller to know which connection goes first
                self.first = 0
                message = 'b'.encode()
                self.connection_socket[1].send(message)
               
                # Confirmation of color selection for client 1
                self.connection_socket[0].send(answer.encode())
                break

            elif answer == 'b': 
                # For game controller to know which connection goes first
                self.first = 1
                message = 'w'.encode()
                self.connection_socket[1].send(message)
                # Confirmation of color selection for client 1
                self.connection_socket[0].send(answer.encode())
                break

            else: 
                message = ('Invalid Input, please try again...').encode()
                self.connection_socket[0].send(message)

        self.start_game()
        time.sleep(7)
        atexit.unregister(self.disconnect)
        self.disconnect()
        
    
    def start_game(self):

        gcont = ServerGameController(self.connection_socket, self.first)
        gcont.start_game()


    def disconnect(self):

        for connection in self.connection_socket:
            if connection:
                connection.close()
        self.server_socket.close()
        print('Connections Closed')
        self.close_port()


    def close_port(self):

        subprocess.call([r'C:\Users\ericd\OneDrive\Desktop\NEU\!Coding\2140\networkedChess\close_port.bat'])