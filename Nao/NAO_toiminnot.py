# -*- coding:utf-8 -*-

import subprocess
import socket
from tkinter import messagebox

RobottiNimi=""
RobottiIP=""
RobottiPort=""
vastaus=""

python27="C:\Python27\python.exe" #Polku Python27.exe luokse.

def testNaoYhteys():
    socket.setdefaulttimeout(1)
    s = socket.socket()
    try:
        s.connect((RobottiIP, int(RobottiPort))) 
        vastaus = True
    except Exception as e:
        vastaus = False
    finally:
        s.close()
    if vastaus == True:
        palaute = "Y"
        return palaute
    elif vastaus == False:
        palaute = "N"
        return palaute
    else:
        palaute = "C"
        return palaute

def suoritaToiminto(koodi):
    suorita = open("suorite.py", "w")
    suorita.write(koodi)
    suorita.close()
    suoritetaan = subprocess.Popen([python27, "suorite.py"])
    pass

def tallennaRobotti():
    robotti = open("RobottiAsetukset.txt", "w")
    rivit = (RobottiNimi, "\n"+str(RobottiIP)+ "\n"+str(RobottiPort)+"\n")
    robotti.writelines(rivit)
    robotti.close()
    
def ViimeisinRobotti():
    try:
        robotti=open("RobottiAsetukset.txt", "r")
        rivit=robotti.readlines()
        RobottiNimi = rivit[0][:-1]
        RobottiIP = rivit[1][:-1]
        RobottiPort = int(rivit[2][:-1])
        robotti.close()
    except:
        print("VIRHE TUO VIIMEISIN ROBOTTI")

def robottti():
    try:
        robotti=open("RobottiAsetukset.txt", "r")
        rivit=robotti.readlines()
        RobottiNimi = rivit[0][:-1]
        RobottiIP = rivit[1][:-1]
        RobottiPort = int(rivit[2][:-1])
        robotti.close()
    except:
        print("VIRHE TUO VIIMEISIN ROBOTTI")