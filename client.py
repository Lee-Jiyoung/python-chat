import socket
import threading
import time
import RSA_LEA
from Crypto.Cipher import PKCS1_OAEP
import ast

host ="127.0.0.1"
port = 4000
lea_key =''

def handle_receive(listen_socket):
    while True:
        try:
            data = listen_socket.recv(1024)
        except:
            print("Disconnected")
            break
        data = RSA_LEA.decryption_LEA(data,lea_key)
        print(data)

def transfer_key(conn):
    global lea_key
    private_key, public_key = RSA_LEA.generate_PEM_key()
    conn.send(public_key)
    lea_key = RSA_LEA.decythion_rsa(private_key,conn.recv(1024))


def setSocket():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((host,port))

    transfer_key(client_socket)
    print("Success chang key")
    print("input your name : ",end='')
    name = input()
    name = RSA_LEA.encryption_LEA(name,lea_key)
    client_socket.send(name)

    receive_thread = threading.Thread(target=handle_receive, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        msg = input()
        if msg == "/q":
            client_socket.send(RSA_LEA.encryption_LEA(msg,lea_key))
            client_socket.close()
            break
        client_socket.send(RSA_LEA.encryption_LEA(msg,lea_key))

if __name__ == '__main__':
    print("start chatting")
    setSocket()    
