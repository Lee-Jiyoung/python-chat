import socket
import threading
import RSA_LEA
from Crypto.PublicKey import RSA
import time

host = "127.0.0.1"
port = 4000
lock = threading.Lock()
user_dic = {}
lea_key =''

def sendMessageToALL(user_name,message,id):
    global user_dic
    if id == 0:
        for user in user_dic.keys():
            conn = user_dic[user]
            conn.send(RSA_LEA.encryption_LEA(message,lea_key))
    else :
        for user in user_dic.keys():
            if user == user_name:
                msg =f'[me]: {message}'
            else :
                msg =f'[{user_name}]: {message}'
            conn = user_dic[user]
            conn.send(RSA_LEA.encryption_LEA(msg,lea_key))


def addUser(user_name, conn):
    global user_dic
    if user_name in user_dic :
        return -1

    user_dic[user_name] = conn
    message = f'++++++++++[{user_name}] has entered.+++++++++++++++++'
    sendMessageToALL(user_name,message,0)

    message = f' ++++ Number of chat participants : [{len(user_dic)}] +++'
    print(message)

def removeUser(user_name):
    global user_dic

    lock.acquire()
    del user_dic[user_name]
    lock.release()
    message = f'++++++[{user_name}] has left.+++++++++++++++++'
    sendMessageToALL(user_name,message,0)
    
    message = f' ++++ Number of chat participants : [{len(user_dic)}] +++'
    print(message)

def messageHandler(user_name):
    global user_dic
    while True:
        conn=user_dic.get(user_name)
        message = conn.recv(1024)
        message = RSA_LEA.decryption_LEA(message,lea_key)
        if message == '/q':
            removeUser(user_name)
            break
        else :
            sendMessageToALL(user_name,message,1)
    conn.close()

def keyExchagne(conn):
    global lea_key
    public_key = conn.recv(1024)
    msg = RSA_LEA.encrython_rsa(lea_key,public_key)
    conn.send(msg)

def a():
    timer=threading.Timer(10,a)
    print("a")
    timer.start()

def setSocket():
    global user_dic
    global lea_key

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind((host,port))
    server_socket.listen(5)

    lea_key = RSA_LEA.generate_lea_key()

    while True:
        try:
            client_socket,addr = server_socket.accept()
        except KeyboardInterrupt:
            message = "Shut down the Server"
            sendMessageToALL("",message,1)
            for conn in user_dic.values():
                conn.close()
            server_socket.close()
            print("Keyboard interrupt!!! Shut down the Server")
            return 0

        keyExchagne(client_socket)

        user = RSA_LEA.decryption_LEA(client_socket.recv(1024),lea_key)
        lock.acquire()  
        addUser(user,client_socket)
        lock.release()

        receive_thread = threading.Thread(target=messageHandler,args=(user,))
        receive_thread.daemon=True
        receive_thread.start()

if __name__ == '__main__':
    setSocket()