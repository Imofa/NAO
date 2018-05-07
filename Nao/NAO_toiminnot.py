# -*- coding:utf-8 -*-

import os
import subprocess

#import naoqi
RobottiNimi=""
RobottiIP="0.0.0.0"
RobottiPort=""
vastaus=""

def testNaoYhteys():
    with open(os.devnull, 'w') as DEVNULL:
        print(RobottiIP)
        try:
            vastaus = subprocess.check_call(
                ['ping', '-n', '1', '-w', '200', RobottiIP],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
#            is_up = True
            print(vastaus)
            if vastaus == 0:
                print(vastaus)
                palaute = "Y"
                return palaute
            elif vastaus == 1:
                print(vastaus)
                palaute = "N"
                return palaute
            else:
                palaute = "C"
                print(vastaus)
                return palaute
        except subprocess.CalledProcessError:
#            is_up = False
            palaute = "N"
            return palaute

def suoritaToiminto(koodi):
    suorita = open("suorite.py", "w")
    suorita.write(koodi)
    suorita.close()
    os.system("suorite.py")
    pass



