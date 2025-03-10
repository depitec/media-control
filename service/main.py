from PinManager import PinManager
import RPi.GPIO as GPIO

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    pin_manager = PinManager()
