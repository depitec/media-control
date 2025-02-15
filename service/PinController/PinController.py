from __future__ import annotations
import RPi.GPIO as GPIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Pin import PinType

class PinController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def register_pin(self, pin_number, pin_type: PinType):
        pass
