import RPi.GPIO as GPIO
import time
from AlphaBot2 import AlphaBot2

Ab = AlphaBot2()

CTR = 7
A = 8
B = 9
C = 10
D = 11

def start_square():
    print("starting square")
    Ab.setMotor(25, 18)
    Ab.forward()
 #   side(1)
    Ab.setMotor(25, 16)
    Ab.forward()
    time.sleep(1)
    Ab.stop()
    time.sleep(2)
    print("turn 1")
    Ab.right()
    time.sleep(.225)
    Ab.stop()
    time.sleep(2)
#    side(2)
    Ab.setMotor(25, 16)
    Ab.forward()
    time.sleep(1)
    Ab.stop()
    time.sleep(2)
    print("turn 2")
    Ab.right()
    time.sleep(.22)
    Ab.stop()
    time.sleep(2)
#    side(3)
    Ab.setMotor(25, 16)
    Ab.forward()
    time.sleep(1)
    Ab.stop()
    time.sleep(2)
    print("turn 3")
    Ab.right()
    time.sleep(.215)
    Ab.stop()
    time.sleep(2)
#    side(4)
    Ab.setMotor(25, 16)
    Ab.forward()
    time.sleep(1)
    Ab.stop()
    time.sleep(2)
    print("turn 4")
    Ab.right()
    time.sleep(.22)
    Ab.stop()
    time.sleep(2)
    Ab.stop()
    print("done")


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CTR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(A,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(B,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(C,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(D,GPIO.IN,GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(A) == 0:
            time.sleep(2)
            start_square()

except KeyboardInterrupt:
	GPIO.cleanup()
