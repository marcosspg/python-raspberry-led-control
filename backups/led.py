import RPi.GPIO as gp
import time
from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process
from _thread import *




HOST = '192.168.1.144';
PORT = 80;
azul = 19
blanco = 13

gp.setwarnings(False)
gp.setmode(gp.BCM)
gp.setup(azul, gp.OUT)
gp.setup(blanco, gp.OUT)
gp.output(azul, gp.LOW)
gp.output(blanco, gp.LOW)

pAzul = gp.PWM(azul, 1000)
pBlanco = gp.PWM(blanco, 1000)
pAzul.start(0)
pBlanco.start(0)

azulEncendido = False;
blancoEncendido = False;

def contestar(conn):
	global azulEncendido;
	global blancoEncendido;
	data = conn.recv(1024)
	if data:
		datos=bytes.decode(data)
		print(datos);
		if datos == "azul":
			if not azulEncendido:
				pAzul.ChangeDutyCycle(100);
				
			else:
				pAzul.ChangeDutyCycle(0);
			print("azul cambia");
			azulEncendido = not azulEncendido;
		if datos == "blanco":
			if not blancoEncendido:
				pBlanco.ChangeDutyCycle(100);
			else:
				pBlanco.ChangeDutyCycle(0);
			print("blanco cambia");
			blancoEncendido = not blancoEncendido;
		conn.send("ok".encode())





if __name__=='__main__':
	with socket(AF_INET, SOCK_STREAM) as s:
		s.bind((HOST, PORT));
		s.listen();
		print("Servidor iniciado");
		while True:
			print("preparado");
			conn, addr = s.accept()
			start_new_thread(contestar, (conn,));