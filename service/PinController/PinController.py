import RPi.GPIO as GPIO

class PinController:
    def __init__(self):
      GPIO.setmode(GPIO.BCM)