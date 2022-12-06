from ctypes import sizeof
import socket
import threading
import time
import sys

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

conexoes = []

def enviar_mensagem_individual(conexao, mensagem):
    conexao['conn'].send(mensagem.encode())
    time.sleep(0.2)

def end_conn(addr):
    global conexoes
    print(f"[DESCONECTANDO] PORT_SERVER: {PORT}, PORT_CLIENT: {addr[1]}")
    for conexao in conexoes:
        if(addr[1] == conexao["addr"][1]):
            enviar_mensagem_individual(conexao, "Você saiu!")
            conexoes.remove(conexao)


def enviar_mensagem_todos(addr, mensagem, size):
    global conexoes
    print(f"[ENVIANDO] Enviando mensagens. Emissor : {{[CLIENT_IP : {addr[0]}] [CLIENT_PORT : {addr[1]}]}} Bytes: {size}")
    for conexao in conexoes:
        if(addr[1] != conexao["addr"][1]):
            enviar_mensagem_individual(conexao, mensagem)

def handle_clientes(conn, addr):
    print(f"[NOVA CONEXAO] PORT_SERVER: {PORT}, PORT_CLIENT: {addr[1]}")
    global conexoes
    nome = False

    while(True):
        msg = conn.recv(1024).decode(FORMATO)
        if(msg):
            if(msg.startswith("nome=")):
                mensagem_separada = msg.split("=")
                nome = mensagem_separada[1]
                mapa_da_conexao = {
                    "conn": conn,   
                    "addr": addr,
                    "nome": nome,
                }
                conexoes.append(mapa_da_conexao)

            elif(msg.startswith("msg=")):
                mensagem_separada = msg.split("=")
                mensagem = nome + "=" + mensagem_separada[1]
                size = sys.getsizeof(mensagem_separada[1])
                enviar_mensagem_todos(addr, mensagem, size)
            
            elif (msg == "close"):
                end_conn(addr)
                break




def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()
    while(True):
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()

start()