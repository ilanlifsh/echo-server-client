import socket
import Protocol as prot
import os
import time

HOST = 'localhost'
PORT = 9098
ADDR = (HOST, PORT)
BUF_SIZE = 2

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('[CONNECTING] Conncting to server : ' + HOST + ':' + str(PORT) + ' ...')
connected = False
print("Server not found, waiting for server connection...")
while not connected:
    try:
        client_socket.connect(ADDR)
        connected = True
        print("[CONNECTED]")
    except Exception as e:
        pass # do nothing, try again

while True:
    try:
        user_input = input('Enter a message to send : ')
        if user_input.lower() == 'exit':
            client_socket.sendall(user_input.encode())
            break

        elif user_input.lower()=="send file":
            while True:
                FILE = input('Enter a file to send : ')
                if FILE.lower()=="exit" :
                    break

                if not FILE:
                    continue

                elif os.path.exists(FILE):
                    client_socket.sendall(b"file")
                try:

                    prot.send_file(socket=client_socket, file_name=FILE)
                    ACK = prot.recv_all(socket=client_socket).decode()
                    if ACK == "ACK":
                        print("File was sent successfully")
                        continue
                except FileNotFoundError:
                    print("There is no such file or directory named: \"" + FILE + "\". Try again!")
                    continue
                except:
                    print("Error sending file... Try again!")
                    continue



        elif user_input == '':
            continue

        elif user_input.lower() != "send file":
            prot.send_all(data=user_input, socket=client_socket)
            rxd = prot.recv_all(socket=client_socket)
            if rxd:
                print('[RECEIVED] : ', rxd.decode('utf-8'))



    except ConnectionRefusedError:
        print("Server not found, waiting for server connection...")
    except ConnectionResetError:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        print("SERVER CONNECTION LOST, waiting for server connection...")
        while not connected:
            try:
                client_socket.connect(ADDR)
                connected = True
                print("[CONNECTED]")
            except Exception as e:
                pass  # do nothing, try again
        continue

    except Exception as e:
        print(e)
        break


input('press enter to close')
client_socket.close()
