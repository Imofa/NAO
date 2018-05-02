import os
import subprocess

#import naoqi
RobottiNimi=None
RobottiIP=None
RobottiPort=None

def testNaoYhteys():
    with open(os.devnull, 'w') as DEVNULL:
        try:
            vastaus = subprocess.check_call(
                ['ping', '-n', '1', RobottiIP],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            is_up = True
        except subprocess.CalledProcessError:
            is_up = False
    if vastaus == 0:
        palaute = "Y"
        return palaute
    elif vastaus == 1:
        palaute = "N"
        return palaute
    else:
        palaute = "C"
        return palaute

