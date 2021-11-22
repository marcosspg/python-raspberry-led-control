import RPi.GPIO as gp
from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process
from socket import socket as sock, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from multiprocessing import Process
from _thread import *
import sys
import threading
import time
import random

HOST = '192.168.1.144';
PORT = 80;

r = 26
g = 21
b = 20

gp.setwarnings(False)
gp.setmode(gp.BCM)
gp.setup(r, gp.OUT)
gp.setup(g, gp.OUT)
gp.setup(b, gp.OUT)
gp.output(r, gp.LOW)
gp.output(g, gp.LOW)
gp.output(b, gp.LOW)

colorGlobal = {"r":"0","g":"0","b":"0"};
pr = gp.PWM(r, 1000)
pg = gp.PWM(g, 1000)
pb = gp.PWM(b, 1000)
pr.start(0)
pg.start(0)
pb.start(0)

procesos = [];


def getNumeroNuevoRango(num):
    return (int("0x"+num, 0)*100)/255


def hexaToNewRange(hexa):
    if(hexa.__len__()==6):
        new = {}
        new["r"] = getNumeroNuevoRango(hexa[0:2]);
        new["g"] = getNumeroNuevoRango(hexa[2:4]);
        new["b"] = getNumeroNuevoRango(hexa[4:6]);
        return new;
    else:
        return None;   


pr.ChangeDutyCycle(0);
pg.ChangeDutyCycle(0);
pb.ChangeDutyCycle(0);


def aplicarColor(_):    
    while True:
        
        if str(colorGlobal["r"]) != "-1":
            maximo = 0;
            if colorGlobal["r"] > colorGlobal["g"] and colorGlobal["r"] > colorGlobal["b"]:
                maximo = colorGlobal["r"]
            elif colorGlobal["g"] > colorGlobal["r"] and colorGlobal["g"] > colorGlobal["b"]:
                maximo = colorGlobal["g"];
            else:
                maximo = colorGlobal["b"];
            for i in range(1,int(maximo)+1, 1):
                try:
                    colR = float(i);
                    colG = float(i);
                    colB = float(i);
                    if i>=colorGlobal["r"]:
                        colR = colorGlobal["r"]
                    if i>=colorGlobal["g"]:
                        colG = colorGlobal["g"]
                    if i>=colorGlobal["b"]:
                        colB = colorGlobal["b"]
                    pr.ChangeDutyCycle(colR);
                    pg.ChangeDutyCycle(colG);
                    pb.ChangeDutyCycle(colB);
                    time.sleep(0.03);
                except:
                    None

            for i in range(int(maximo), 0, -1):
                try:
                    colR = float(i);
                    colG = float(i);
                    colB = float(i);
                    if i>=colorGlobal["r"]:
                        colR = colorGlobal["r"]
                    if i>=colorGlobal["g"]:
                        colG = colorGlobal["g"]
                    if i>=colorGlobal["b"]:
                        colB = colorGlobal["b"]
                    pr.ChangeDutyCycle(colR);
                    pg.ChangeDutyCycle(colG);
                    pb.ChangeDutyCycle(colB);
                    time.sleep(0.03);
                except:
                    None
                
            time.sleep(0.4);
        else:
            colorRandom = {"r":random.randint(10,90), "g":random.randint(10,90), "b":random.randint(10,90)};
            maximo = 0;
            if colorRandom["r"] > colorRandom["g"] and colorRandom["r"] > colorRandom["b"]:
                maximo = colorRandom["r"]
            elif colorRandom["g"] > colorRandom["r"] and colorRandom["g"] > colorRandom["b"]:
                maximo = colorRandom["g"];
            else:
                maximo = colorRandom["b"];
            for i in range(1,int(maximo)+1, 1):
                try:
                    colR = float(i);
                    colG = float(i);
                    colB = float(i);
                    if i>=colorRandom["r"]:
                        colR = colorRandom["r"]
                    if i>=colorRandom["g"]:
                        colG = colorRandom["g"]
                    if i>=colorRandom["b"]:
                        colB = colorRandom["b"]
                    pr.ChangeDutyCycle(colR);
                    pg.ChangeDutyCycle(colG);
                    pb.ChangeDutyCycle(colB);
                    time.sleep(0.04);
                except:
                    None
            for i in range(int(maximo), 0, -1):
                try:
                    colR = float(i);
                    colG = float(i);
                    colB = float(i);
                    if i>=colorRandom["r"]:
                        colR = colorRandom["r"]
                    if i>=colorRandom["g"]:
                        colG = colorRandom["g"]
                    if i>=colorRandom["b"]:
                        colB = colorRandom["b"]
                    pr.ChangeDutyCycle(colR);
                    pg.ChangeDutyCycle(colG);
                    pb.ChangeDutyCycle(colB);
                    time.sleep(0.04);
                except:
                    None
            time.sleep(0.4);



def contestar(conn):
    data = conn.recv(1024)
    if data:
        datos=bytes.decode(data)
        color = datos
        global colorGlobal;
        tosend = "ok    ";
        
        if color[0:1] == "#" and color.__len__()==7:
            newColor = hexaToNewRange(color[1:]);       
            colorGlobal = (newColor);
        elif color == "azuloscuro":
            colorGlobal = hexaToNewRange("0000ff");
        elif color == "azulclaro":
            colorGlobal = hexaToNewRange("26e8ff");
        elif color == "rojo":
            colorGlobal = hexaToNewRange("ff0000");
        elif color == "verde":
            colorGlobal = hexaToNewRange("00ff00");
        elif color == "morado":
            colorGlobal = hexaToNewRange("bd00da");
        elif color == "apagado":
            colorGlobal = hexaToNewRange("000000");
        elif color == "random":
            colorGlobal = {"r":-1, "g":-1, "b":-1};
        else:
            tosend = "colorinvalido";
        conn.send(tosend.encode())


if __name__=='__main__':
    start_new_thread(aplicarColor, (None,));
    with socket(AF_INET, SOCK_STREAM) as s:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((HOST, PORT));
        s.listen();
        print("Servidor iniciado");
        iniciar = True;
        while iniciar:
            conn, addr = s.accept()
            contestar(conn);
        s.close();
        sys.exit()
          