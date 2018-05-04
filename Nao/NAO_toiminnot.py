# -*- coding:utf-8 -*-

import os
import subprocess

#import naoqi
RobottiNimi=""
RobottiIP=""
RobottiPort=""
vastaus=""

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
            is_up = True
        except subprocess.CalledProcessError:
            is_up = False
            palaute = "N"
            return palaute

def suoritaToiminto(koodi):
    suorita = open("suorite.py", "w")
    suorita.write(koodi)
    suorita.close()
    os.system("suorite.py")
    pass



