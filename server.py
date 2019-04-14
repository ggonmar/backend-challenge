import json
import socket
import sys
import threading

from cart import Cart

verbose: bool = True        # boolean to control the amount of output on logs that both Client and Server will have
timeout_server: int = 60    # Time inactive until client is disconnected
PORT: int = 8888            # port on which the server will be listening


# Class Server:
# This class will handle the initialization of the server,
# as well as the threading to be able to attend to different clients

class Server(object):

    # Initializer, definition of the socket and binding
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cart = {}
        print('[Server] Socket created')

        try:
            self.sock.bind((self.host, self.port))
        except socket.error as msg:
            print(f'[Server] Bind failed. Error code : {msg[0]} - Message {msg[1]}')
            sys.exit()
        print('[Server] Socket Bind complete')

    # Method that will await for incoming connections from clients.
    # When a connection request is received, a new dedicated thread of the method "attend" is started
    def listen(self):
        self.sock.listen(10)
        while True:
            conn, addr = self.sock.accept()
            conn.settimeout(timeout_server)
            threading.Thread(target=self.attend, args=(conn, addr)).start()

    # Handler of the shopping experience once the connection has been established.
    def attend(self, conn, addr):
        connection_id = addr[0] + ":" + str(addr[1])  # Defining uniqueness by ip:port duplet

        print(f'[Server][{connection_id}] Connection established')

        self.cart = Cart()  # A new cart object is created for the new customer
        try:
            # On a loop, the server (in this case, "attendant") receives every request from client.
            # it then processes the request on the cart using the cart.process_request()
            # And returns the current status of the cart.
            while True:
                request_from_client = conn.recv(1).decode()
                print(f'[Server][{connection_id}] Received {request_from_client}')

                # answer is a dictionary with keys:
                #    - "response" informing about the successful addition of the request
                #    - "current cart" a straight forward compute of the cart
                answer = json.dumps(self.cart.process_request(request_from_client, verbose))

                conn.sendall((f'{answer}\nEOM').encode())

                # if request is to exit, we exit the loop
                if request_from_client == '0':
                    break

        # In all cases, we finalize the connection after serving the client
        finally:
            print(f'[Server][{connection_id}] Connection finished by client')
            conn.close()
            return False


Server('', PORT).listen()

