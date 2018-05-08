# -*- coding:utf-8 -*-

import os
import subprocess

#import naoqi
RobottiNimi=""
RobottiIP="0.0.0.0"
RobottiPort=""
vastaus=""

python27="C:\Python27\python.exe"

def testNaoYhteys():
    with open(os.devnull, 'w') as DEVNULL:
        try:
            vastaus = subprocess.check_call(
                ['ping', '-n', '1', '-w', '200', RobottiIP],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            if vastaus == 0:
                palaute = "Y"
                return palaute
            elif vastaus == 1:
                palaute = "N"
                return palaute
            else:
                palaute = "C"
                return palaute
        except subprocess.CalledProcessError:
            palaute = "N"
            return palaute

def suoritaToiminto(koodi):
    suorita = open("suorite.py", "w")
    suorita.write(koodi)
    suorita.close()
    suoritetaan = subprocess.Popen([python27, "suorite.py"])
#    os.system("suorite.py")
    pass



