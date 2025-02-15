import RPi.GPIO as GPIO
from .Pin import PIN_TYPE, Pin


class PinController:
    def __init__(self):
        self.pins = {}
        GPIO.setmode(GPIO.BCM)

    def register_pin(self, pin_number: int, pin_type: PIN_TYPE):
        GPIO.setup(
            pin_number, pin_type.value
        )  # using the value of the enum to satisfy the type checker
        self.pins[pin_number] = Pin(self, pin_number, pin_type)

    def unregister_pin(self, pin_number: int):
        GPIO.cleanup(pin_number)
        del self.pins[pin_number]
