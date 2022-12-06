from glob import glob
from pyclbr import Class
import socket
import threading
import time

PORT = 5050
FORMATO = 'utf-8'
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def handle_mensagens():
    while(True):
        msg = client.recv(1024).decode()
        if(msg == "Você saiu!"):
            print(msg)
            break
        else:
            mensagem_splitada = msg.split("=")
            print(mensagem_splitada[0] + ": " + mensagem_splitada[1])

def enviar_mensagem(mensagem):
        client.send(mensagem.encode(FORMATO))

def iniciar():
    thread1 = threading.Thread(target=handle_mensagens)
    thread1.start()
    while(True):
        mensagem = input()
        if(mensagem == ""):
            enviar_mensagem("msg=" + "Saiu!")
            enviar_mensagem("close")
            break
        enviar_mensagem("msg=" + mensagem)


nome = input('Digite seu nome: ')
enviar_mensagem("nome=" + nome)
enviar_mensagem("msg=" + "Entrou no grupo!")


iniciar()
client.close