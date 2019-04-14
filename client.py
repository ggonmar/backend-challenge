import json
import sys
import time
import socket

N: int = 1   # Waiting time between requests - Interesting for seeing the responses from the Server


# function that displays the initial menu for the client, prompting them to choose what to buy
# and filtering for correct options only.
# On the header of the menu, one may see the summary of the cart that has been so far added.

def print_menu(current_cart=''):
    current_cart_line = f'|  Current Cart: {current_cart}' if current_cart != "" else ""
    while 1:
        print(f'''
WELCOME TO CABIFY STORE  {current_cart_line}
Choose your element to be added to the cart
 1. Voucher (5€)
 2. T Shirt (20€)
 3. Mug (7.5€) 
 
 Or Benefit from our special deals!
  8. 2x1 on Vouchers ( 2 for 5€ ) 
  9. 5% off on every 3 shirts ( 19€ each when buying 3 )
 
  0. Pay and Exit
 ----''')

        choice = input('    Your Choice: ')
        if choice in ('1', '2', '3', '8', '9', '0'):
            return choice
        else:
            print('Invalid input. Resetting')
            time.sleep(N)
            for i in range(1, 5):
                print('')


# Setup of the connection to the Server. Error handling in case the Server is not available.
def setup_connection(host, port):
    try:
        s: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (host, port)
        print('[Client] Connecting to %s:%s' % server_address)
        s.connect(server_address)
        return s
    except socket.error:
        print('[Client] Connection refused')
        sys.exit()


# Function to display the response from the server after a request has been made.
def propose_proceed(response):
    print(f'[Client] {response}')
    time.sleep(N)
    for i in range(1, 10):
        print('')


# Client main function. Starts the connection, and prompts the user for what actions to take on a loop.
# Each selection is sent to the server, and client prints out the response received.
# The response consists of a duplet:
#   - The confirmation to the last request done
#   - A summary of the cart to be embedded on the menu

def start_client():
    socket = setup_connection('localhost', 8888)
    current_cart = ''

    try:
        while True:
            selection = print_menu(current_cart)

            # Processing request
            if selection != '0':
                print(f'[Client] Adding selection {selection} to  cart')

            # Contacting Server to process request
            socket.sendall(selection.encode())

            # Obtaining response
            received = ''
            while received[-3:] != 'EOM':
                received += socket.recv(50).decode()
            received = json.loads(received[:-3])

            # Parsing response
            ack_request = received["response"]
            current_cart = received["current_cart"]

            # If user requested to End, the response is a receipt. Print it and exit.
            if selection != '0':
                propose_proceed(ack_request)
            else:
                print('[Client] Requesting receipt')
                print(f'[Client] Final Receipt is: {ack_request}')
                time.sleep(N)
                break

    # Error handling
    except:
        print('[Client] Connection timed out')
        return False

    # In all cases, close the connection
    finally:
        try:
            socket.close()
        except NameError:
            print('[Client] Connection closed')


start_client()
