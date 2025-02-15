from PinController import PinController
import RPi.GPIO as GPIO

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    pin_controller = PinController()
