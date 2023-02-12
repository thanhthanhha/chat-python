import socket
import sys
import errno
import msvcrt
import logging
import selectors
import types

logging.basicConfig(filename='client.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')
sel = selectors.DefaultSelector()

def main():
    Host, Port = str(sys.argv[1]),int(sys.argv[2])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex((Host, Port))
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
            msg_total=0,
            recv_total=0,    
    )
    sel.register(sock, events, data=data)
    data_to_write = ''
    user_input = ''

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                sock = key.fileobj
                data = key.data
                if mask & selectors.EVENT_READ:
                    data_input = socket_nonblocking_input(sock)
                    data_input = data_input.decode()
                    print(data_input)
                if mask & selectors.EVENT_WRITE and data_to_write:
                    data_to_send = data_to_write.encode()
                    print(f'<You>: {data_to_write}')
                    data_byte = socket_nonblocking_output(sock, data_to_send)
                    data_to_write = data_byte.decode('utf-8')
                if msvcrt.kbhit():
                    key = msvcrt.getche()
                    if key == b"\r":
                        logging.debug(f'user input {user_input}')
                        data_to_write += user_input
                        user_input = ''
                    else:
                        user_input += key.decode('utf-8') 

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()




def raw_nonblocking_output() -> str:
        user_input = ""
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getche()
                if key == b"\r":
                    logging.debug(f'user input {user_input}')
                    return user_input
                else:
                    user_input += key.decode('utf-8') 

def socket_nonblocking_input(sock):
    try:
        msg = sock.recv(2024)
    except socket.error as e:
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            return ''
        else:
            raise
    logging.debug(f'server sent us {msg}')
    if not msg:
        raise SystemExit
    return msg

def socket_nonblocking_output(sock, msg):
    try:
        res = sock.send(msg)
    except socket.error as e:
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            return msg
        else:
            raise
    if not res:
        raise SystemExit
    logging.debug("we have sent %d bytes out of %d" % (res, len(msg)))
    return msg[res:]

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        pass

