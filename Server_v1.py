import socket
import Protocol as prot
from Protocol import HEADER_SIZE  # Import the header size for protocol use
import subprocess  # For launching external applications (like Paint or Media Player)

# Define server host, port, and address
HOST = 'localhost'
PORT = 9098
ADDR = (HOST, PORT)
BUF_SIZE = 1024  # Buffer size for receiving data
PAINT_PATH = r"C:\YOUR\PATH\TO\mspaint.exe"  # Path to MS Paint
MEDIA_PLAYER = r"C:\YOUR\PATH\TO\wmplayer.exe"  # Path to Windows Media Player

# Create and configure the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)  # Bind the socket to the address and port
server_socket.listen(5)  # Set up the server to listen for connections, with a backlog of 5 clients

print(f"Server Ready, Waiting for client on {ADDR}")
client_socket, client_addr = server_socket.accept()  # Wait for a client to connect
print(f"New client connected on {client_addr}")

# Main loop for handling communication with the client
while True:
    try:
        data = client_socket.recv(BUF_SIZE)  # Receive data from the client

        if not data:
            # If no data is received (client disconnected), close the connection and wait for a new client
            client_socket.close()
            server_socket.listen(5)  # Re-listen for new client
            print(f"Server Ready, Waiting for client on {ADDR}")
            client_socket, client_addr = server_socket.accept()  # Accept new connection
            print(f"New client connected on {client_addr}")
            continue

        elif data.decode() == 'exit':  # If the client sends 'exit', break the loop to close the server
            break

        # If the client sends 'file', handle the file
        if data.decode().lower() == "file":
            # Receive the file from the client using the protocol's recv_file function
            file_name = prot.recv_file(socket=client_socket)
            if file_name is not None:
                # Check the file extension and open with appropriate application
                if file_name.lower().endswith(('.jpg', '.png', '.gif')):
                    # Open image files with MS Paint
                    subprocess.run([PAINT_PATH, file_name])

                elif file_name.lower().endswith(('.mp3', '.mp4')):
                    # Open media files with Windows Media Player
                    subprocess.run([MEDIA_PLAYER, file_name])

                # Send acknowledgment back to the client
                ACK = "ACK"
                prot.send_all(data=ACK, socket=client_socket)
                print(f"[SEND TO CLIENT]: {ACK}")

        elif data:
            # If other data is received (not a file or 'exit'), print and send it back to the client
            print(f"[RECEIVED FROM CLIENT AT] {client_addr}: {data[HEADER_SIZE:].decode('utf-8')}")
            client_socket.sendall(data)  # Send the received data back to the client
            print(f"[SEND TO CLIENT]: {data[HEADER_SIZE:].decode()}")

    except Exception as e:
        # Catch and print any exceptions, then break the loop
        print(e)
        break

# Close the sockets when the communication ends
input("press any key to close")
server_socket.close()  # Close the server socket
client_socket.close()  # Close the client socket

