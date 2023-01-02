# This file is intended to initialize the client side of the chess game

from mvc.Controller.client_game_controller import ClientGameController
import socket

class Chess_Client():
    
    def __init__(self) -> None:
        
        # Initialize variables
        server_address = '192.168.2.240'
        server_port_number = 12002
        server_identifier = (server_address, server_port_number)

        # Create client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Client socket created...')

        # Change default timeout
        self.client_socket.settimeout(30)

        # Connect to the Server
        self.client_socket.connect(server_identifier)
        
        # Receive initial message from server
        print(self.client_socket.recv(1024).decode())

        # Receive and Dissect server message
        while True:
            message = self.client_socket.recv(1024).decode()
            print(message)
            message = message.split()
            if (message == 'b') or (message == 'w'):
                self.color = message
                print(f'You are {message}')
                break
            elif message[0] == 'Choose':
                response = (input(message)).encode()
                self.client_socket.send(response)
            elif message[0] == 'Invalid':
                print(message)  
        
        self.start_game()
        self.disconnect()
    

    def send_move(self, message):

        self.client_socket.send(message.encode())

    
    def receive_packet(self):

        return self.client_socket.recv(2048).decode()  
          
    
    def disconnect(self):

        self.client_socket.close()


    def start_game(self):

        gcont = ClientGameController(self.color, self.client_socket)