File Transfer Application
This project allows file transfer between a client and a server using Python's socket programming. It includes several scripts that enable the client to connect to the server, send messages, upload/download files, and handle various socket-related operations. The server handles the incoming connection, receives and processes messages, and manages the reception of files.

File Overview
client.py: The client-side application that allows the user to interact with the server by sending messages and files.
server.py: The server-side application that accepts incoming client connections, handles messages, and processes file transfers.
Protocol.py: Contains the functions used for sending and receiving data (both messages and files) between the client and server.
README.md: This file, which describes the project, its components, and how to use it.
Setup Instructions
To run the project, follow these steps:

1. Prerequisites
Ensure you have Python installed (preferably Python 3.x). The code uses standard Python libraries (socket, os, subprocess), so no external dependencies are required.

2. Running the Server
Navigate to the folder containing the server.py file.
Run the server script using the command:
bash
Copy code
python server.py
The server will listen on port 9098 (by default). Once a client connects, the server will be ready to send and receive files or messages.
3. Running the Client
Navigate to the folder containing the client.py file.
Run the client script using the command:
bash
Copy code
python client.py
The client will connect to the server running on localhost:9098. The user can send messages, upload files, or exit the connection.
File Breakdown
client.py
This script is the client-side application that connects to the server and allows the user to interact with it. The client can:

Send text messages to the server.
Upload files to the server.
Download files (handled automatically by the server).
Disconnect by typing exit.
Key functions:
connect_to_server(): Establishes a connection with the server.
send_message(message): Sends a message to the server.
send_file(file_path): Sends a file to the server.
disconnect(): Closes the connection to the server when exit is typed.
server.py
This script is the server-side application that listens for incoming client connections and processes requests. The server can:

Receive messages from the client.
Accept file uploads and open them with the appropriate program (e.g., images open in MS Paint, media files play in Windows Media Player).
Key functions:
client_connection(): Accepts a connection from a client.
handle_client(): Processes messages and files from the connected client.
Handles file reception and opens files based on their extensions.
Protocol.py
This module contains utility functions for sending and receiving data (messages and files) between the client and the server.

Key functions:
send_all(socket, data): Sends data to the client, including a header that specifies the length of the data.
recv_all(socket): Receives data from the client, including the message length header.
send_file(socket, file_name): Sends a file from the client to the server.
recv_file(socket): Receives a file from the client and saves it on the server.
Constants
HEADER_SIZE: The size of the header that stores the length of the message being sent/received.
BUF_SIZE: The size of the buffer used when reading/writing data.
FILE_HEADER: The size of the header for storing the file name.
Usage
Client Usage:
When the client starts, it will automatically attempt to connect to the server at localhost:9098.
The client will prompt the user to enter commands.
Available commands:
send file: Allows the user to upload a file to the server.
exit: Disconnects the client from the server.
Any other message is treated as a regular text message sent to the server.
Server Usage:
The server listens for incoming connections on port 9098.
Once a client connects, the server will process any incoming messages.
If the server receives a file, it will save the file and attempt to open it with the appropriate application based on the file extension:
.jpg, .png, .gif: Opens with MS Paint.
.mp3, .mp4: Opens with Windows Media Player.
If the connection is closed or lost, the server will continue to listen for new clients.
Example Flow
Client Side:
mathematica
Copy code
Enter a message to send: Hello Server!
[RECEIVED]: Hello Server!

Enter a message to send: send file
Enter a file to send: C:\path\to\file.mp4
File was sent successfully.

Enter a message to send: exit
Server Side:
vbnet
Copy code
Server Ready, Waiting for client on ('localhost', 9098)
New client connected on ('127.0.0.1', 12345)
[RECEIVED FROM CLIENT]: Hello Server!
[SEND TO CLIENT]: Hello Server!

[SEND TO CLIENT]: ACK
New client connected on ('127.0.0.1', 12345)
...
Troubleshooting
Connection Refused/Server Not Found:

Ensure the server is running before starting the client.
Check that the server is listening on the correct port (9098).
File Transfer Issues:

Verify that the file exists and the file path is correct.
Ensure that the client has permission to read and send the file.
Check that the server is able to write to the upload directory.
Unsupported File Types:

The server only supports opening .jpg, .png, .gif, .mp3, and .mp4 files by default. You can modify server.py to support other file types if needed.
