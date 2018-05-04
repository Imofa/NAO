# Tiedoston nimi: Walk.py
from naoqi import ALProxy
IP = "127.0.0.1"
PORT = 52495
motion = ALProxy("ALMotion", IP, PORT) #motion, olio, liike
motion.setStiffnesses("Body", 1.0)
tts = ALProxy("ALTextToSpeech", IP, PORT) #tts olio, puhe
motion.moveInit()
id=motion.post.moveTo(0.5, 0, 0) #0.5m x-suunnassa
motion.wait(id,0)
tts.say("I have reached my destination!")



