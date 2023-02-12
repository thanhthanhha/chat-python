import socket
import select
import sys
import traceback
import msvcrt
import logging
import selectors

logging.basicConfig(filename='client.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

def socket_nonblocking_output():
        user_input = ""
        key = msvcrt.getche().decode()
        if key == "\r":
            user_input = user_input.encode()
            logging.debug('user input [%s]' % user_input)
            return user_input
        else:
            user_input += key

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        exit()

    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])

    

    server.connect((IP_address,Port))
    try: 
        while True:
            try: 
                socklist = [server]
                soread, sowrite, soerr = select.select(socklist,[],[],0.5)

                for socks in soread:
                    if socks == server:
                        message = server.recv(2048)
                        byt = message.decode()
                        print(byt)
                if msvcrt.kbhit():
                    user_input = ""
                    key = msvcrt.getche().decode()
                    if key == "\r":
                        byt_input = user_input.encode()
                        server.send(byt_input)
                        print("\nYou: " + user_input)
                        user_input = ""
                    else:
                        user_input += key
            except Exception as ex:
                    print("======> Fatal Error....\n" + str(ex))
                    print(traceback.format_exc())
                    server.close()
                    raise
    except (SystemExit, KeyboardInterrupt):
        print("Server closed with KeyboardInterrupt!")
        server.close()
        raise

    server.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        pass

