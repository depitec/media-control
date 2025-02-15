import RPi.GPIO as GPIO
from .Pin import Pin, PinType


class PinController:
    def __init__(self):
        self.pins = {}
        GPIO.setmode(GPIO.BCM)

    def register_pin(self, pin_number: int, pin_type: PinType):
        direction = GPIO.OUT if pin_type == "output" else GPIO.IN

        GPIO.setup(pin_number, direction)

        self.pins[pin_number] = Pin(self, pin_number, pin_type)

    def unregister_pin(self, pin_number: int):
        GPIO.cleanup(pin_number)
        del self.pins[pin_number]
