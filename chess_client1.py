# This file is intended to initialize the client side of the chess game

from mvc.Controller.client_game_controller1 import ClientGameController
import socket
import time
import atexit

class Chess_Client():
    
    def __init__(self) -> None:
        
        # Initialize variables
        server_address = '155.33.81.197'
        server_port_number = 12004
        server_identifier = (server_address, server_port_number)

        # Create client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Client socket created...')
        atexit.register(self.disconnect)

        # Change default timeout
        self.client_socket.settimeout(30)

        # Connect to the Server
        count = 0
        while True:
            try:
                self.client_socket.connect(server_identifier)
                # Receive initial message from server
                message = 0
                message = self.client_socket.recv(1024).decode()
                print(message)

            except TimeoutError as e:
                if count < 4:
                    print('Connection failed, trying again...')
                    count += 1
                else:
                    print('Connection denied, exiting program')
                    exit()
                continue

            else: 
                if not message:
                    print('Unknown error')
                else: break

        # Receive and Dissect server message
        while True:

            message = self.client_socket.recv(1024).decode()
            print('Received message:\n' + message)
            unchanged_message = message
            message = message.split()

            if (message[0] == 'b') or (message[0] == 'w'):
                self.color = unchanged_message
                print(f'You are {unchanged_message}')
                break
            elif message[0] == 'Choose':
                response = input().encode()
                self.client_socket.send(response)
            elif message[0] == 'Invalid':
                print(message)  
        
        self.start_game()
        time.sleep(5)
        atexit.unregister(self.disconnect)
        self.disconnect()
    

    def disconnect(self):

        self.client_socket.close()
        print('Connections Closed')


    def start_game(self):

        gcont = ClientGameController(self.color, self.client_socket)
        gcont.start_game()