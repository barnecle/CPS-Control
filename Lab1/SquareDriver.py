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
    side(1)
    side(2)
    side(3)
    side(4)
    Ab.stop()
    print("done")

def side(x):
    Ab.forward()
    time.sleep(1)
    print("turn "+ str(x))
    Ab.right()
    time.sleep(1)

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
			start_square()

except KeyboardInterrupt:
	GPIO.cleanup()
