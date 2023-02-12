import socket
import select
import traceback
import sys
import os
from _thread import *

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if len(sys.argv) != 3:
        print("Correct usage: script, IP Address, port number")
        print(sys.argv)
        exit()

    IP_address = str(sys.argv[1])

    Port = int(sys.argv[2])

    server.bind((IP_address,Port))
    server.listen(100)
    server.settimeout(0.5)

    list_of_clients = []

    def clientthread(conn,addr):
        flag = "Welcome to chatroom".encode()
        conn.send(flag)

        while True:
            try:
                message = conn.recv(2048)
                if message:
                    byt = message.decode()
                    print("<" + addr[0] + ">" + byt)
                    message_to_send = "<" + addr[0] + ">" + byt
                    broadcast(message_to_send,conn)
                else:
                    remove(conn)
            except:
                continue
    def broadcast(message,connection):
        for client in list_of_clients:
            if client != connection:
                try:
                    byt = message.encode()
                    client.send(byt)
                except:
                    client.close()
                    remove(client)

    def remove(connection):
        if connection in list_of_clients:
            list_of_clients.remove(connection)

    try: 
        while True:
            try: 
                conn, addr = server.accept()
                list_of_clients.append(conn)
                print(addr[0] + " Connected")
                start_new_thread(clientthread,(conn,addr))
            except(SystemExit, KeyboardInterrupt):
                print("Exiting....")
                stop_service(IP_address, Port)
                break
            except socket.timeout:
                pass
            except Exception as ex:
                print("======> Fatal Error....\n" + str(ex))
                print(traceback.format_exc())
                stop_service(IP_address, Port)
                raise
    except (SystemExit, KeyboardInterrupt):
        print("Force Exiting....")
        server.close()
        raise

    conn.close()
    server.close()

def stop_service(IP_address, Port):
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((IP_address, Port))
    socket.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        pass