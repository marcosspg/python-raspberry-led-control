import RPi.GPIO as gp
from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process
from _thread import *



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


pr = gp.PWM(r, 1000)
pg = gp.PWM(g, 1000)
pb = gp.PWM(b, 1000)
pr.start(0)
pg.start(0)
pb.start(0)



def getNumeroNuevoRango(num):
    #OldRange = (255 - 0)  
    #NewRange = (100 - 0)  
    #return (((int("0x"+num, 0) - 0) * NewRange) / OldRange) + 0
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





while True:
    color = input("Color: ");
    intensidad = "";
    
    if color[0:1] == "#" and color.__len__()==7:
        
        newColor = hexaToNewRange(color[1:]);       
        pr.ChangeDutyCycle(0);
        pg.ChangeDutyCycle(0);
        pb.ChangeDutyCycle(0);
        pr.ChangeDutyCycle(float(newColor["r"]));
        pg.ChangeDutyCycle(float(newColor["g"]));
        pb.ChangeDutyCycle(float(newColor["b"]));
        print(newColor)
    else:
        intensidad =  input("Intensidad 0-100: ");
        if color=="r":
            pr.ChangeDutyCycle(float(intensidad));
        elif color == "g":
            pg.ChangeDutyCycle(float(intensidad));
        else:
            pb.ChangeDutyCycle(float(intensidad));

