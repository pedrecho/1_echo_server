import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"
client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

logs = f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}\n"


def listen_for_client(cs):
    global logs
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            logs += f"[!] Error: {e}\n"
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ": ")
        finally:
            logs += msg + '\n'
        for client_socket in client_sockets:
            client_socket.send(msg.encode())


def new_client():
    global logs
    while True:
        client_socket, client_address = s.accept()
        logs += f"[+] {client_address} connected.\n"
        client_sockets.add(client_socket)
        t = Thread(target=listen_for_client, args=(client_socket,))
        t.start()


def main():
    global logs
    c = Thread(target=new_client)
    c.start()
    while True:
        s = input()
        if s == "end":
            return
        if s == "logs":
            print(logs)
        if s == "clear":
            logs = ""


main()
for cs in client_sockets:
    cs.close()
s.close()