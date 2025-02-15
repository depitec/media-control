from __future__ import annotations
from typing import TYPE_CHECKING
import RPi.GPIO as GPIO
import enum

if TYPE_CHECKING:
    from .PinController import PinController


class PIN_STATE(enum.Enum):
    ACTIVE = 1
    INACTIVE = 0


class PIN_TYPE(enum.Enum):
    INPUT = GPIO.IN
    OUTPUT = GPIO.OUT


class PIN_TRIGGER_TYPE(enum.Enum):
    IMPULSE = 1
    HOLD = 2


class Pin:
    def __init__(
        self,
        controller: PinController,  # fixed value never change
        gpio_pin: int,  # fixed value never change
        pin_type: PIN_TYPE = PIN_TYPE.INPUT,  # fixed value never change
        trigger_type: PIN_TRIGGER_TYPE = PIN_TRIGGER_TYPE.IMPULSE,
        trigger_hold_time: int = 5,  # in seconds
        is_blocked: bool = False,
    ):
        self.controller = controller
        self.gpio_pin = gpio_pin
        self.type = pin_type
        self.is_blocked = is_blocked
        self.trigger_type = trigger_type
        self.trigger_hold_time = trigger_hold_time

    def change_trigger_type(self, trigger_type: PIN_TRIGGER_TYPE):
        if trigger_type == self.trigger_type:
            return
        self.trigger_type = trigger_type

    def change_trigger_hold_time(self, trigger_hold_time: int):
        if trigger_hold_time == self.trigger_hold_time:
            return
        self.trigger_hold_time = trigger_hold_time

    def change_blocked_state(self, is_blocked: bool):
        if is_blocked == self.is_blocked:
            return
        self.is_blocked = is_blocked
