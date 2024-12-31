import socket
import Protocol as prot  # Import Protocol module for sending/receiving data
import os
import time

# Define host and port for the server connection
HOST = 'localhost'
PORT = 9098
ADDR = (HOST, PORT)  # Combine host and port into an address tuple
BUF_SIZE = 2  # Buffer size for receiving data (for sending data in chunks later in protocol)

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try connecting to the server
print('[CONNECTING] Connecting to server : ' + HOST + ':' + str(PORT) + ' ...')
print("Server not found, waiting for server connection...")
connected = False
while not connected:
    try:
        client_socket.connect(ADDR)  # Attempt to connect to the server
        connected = True
        print("[CONNECTED]")  # Success message
    except Exception as e:
        pass  # If connection fails, silently retry

# Main loop for interacting with the server
while True:
    try:
        # Get user input for sending a message or command
        user_input = input('Enter a message to send : ')

        # If user enters 'exit', disconnect from the server
        if user_input.lower() == 'exit':
            client_socket.sendall(user_input.encode())  # Send 'exit' to server
            break  # Exit the loop and disconnect

        # If user chooses to send a file
        elif user_input.lower() == "send file":
            while True:
                # Get file path from user
                FILE = input('Enter a file to send : ')
                if FILE.lower() == "exit":
                    break  # Exit the file sending loop if user enters 'exit'

                if not FILE:
                    continue  # Skip if no file path is entered

                elif os.path.exists(FILE):  # Check if file exists
                    client_socket.sendall(b"file")  # Notify server to expect a file
                    try:
                        # Send the file using the Protocol's send_file function
                        prot.send_file(socket=client_socket, file_name=FILE)
                        ACK = prot.recv_all(socket=client_socket).decode()  # Wait for acknowledgment from the server
                        if ACK == "ACK":
                            print("File was sent successfully")
                            continue  # Continue if file was sent successfully
                    except FileNotFoundError:
                        print("There is no such file or directory named: \"" + FILE + "\". Try again!")
                        continue  # Retry if the file isn't found
                    except:
                        print("Error sending file... Try again!")
                        continue  # Retry in case of any error while sending the file

        # Skip if the user entered an empty string
        elif user_input == '':
            continue

        # If user enters a normal message, send it to the server
        elif user_input.lower() != "send file":
            prot.send_all(data=user_input, socket=client_socket)  # Send the message to the server
            rxd = prot.recv_all(socket=client_socket)  # Wait for a response from the server
            if rxd:  # If response is received, print it
                print('[RECEIVED] : ', rxd.decode('utf-8'))

    # Handle server connection issues
    except ConnectionRefusedError:
        print("Server not found, waiting for server connection...")  # Server is not available
    except ConnectionResetError:
        # Handle the case where the server forcibly closes the connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Recreate socket
        connected = False
        print("SERVER CONNECTION LOST, waiting for server connection...")
        while not connected:
            try:
                client_socket.connect(ADDR)  # Attempt to reconnect
                connected = True
                print("[CONNECTED]")  # Successfully reconnected
            except Exception as e:
                pass  # If connection fails, silently retry
        continue  # Continue the loop after reconnecting

    except Exception as e:
        print(e)  # Print any other unexpected errors
        break

# Close the socket connection when done
input('Press enter to close')
client_socket.close()
