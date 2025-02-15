from __future__ import annotations
from typing import TYPE_CHECKING
import RPi.GPIO as GPIO
import enum

if TYPE_CHECKING:
    from .PinController import PinController


class PinState(enum.Enum):
    ACTIVE = 1
    INACTIVE = 0


class PinType(enum.Enum):
    INPUT = GPIO.IN
    OUTPUT = GPIO.OUT


class Pin:
    def __init__(self, controller: PinController, gpio_pin, type):
        self.controller = controller
        self.gpio_pin = gpio_pin
        # setup pin

        self.state: PinState = PinState.INACTIVE
