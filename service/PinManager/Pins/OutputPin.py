from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Literal
from .Pin import Pin

if TYPE_CHECKING:
    from ..PinManager import TriggerContext

import RPi.GPIO as GPIO

type OutputTriggerMethodName = Literal["pulse", "hold", "while_input"]


class OutputPin(Pin):
    trigger_method_name: OutputTriggerMethodName
    hold_time: float

    def __init__(
        self,
        name: str,
        gpio_pin: int,
        trigger_type: OutputTriggerMethodName = "pulse",
        hold_time: float = 5,
    ):
        super().__init__(name, gpio_pin, "output")
        self.trigger_method_name = trigger_type
        self.hold_time = hold_time

    def trigger(self, context: TriggerContext):
        self.trigger_start()
        if self.is_blocked:
            return
        self.activate(context)
        self.deactivate()
        self.trigger_end()

    def activate(self, context: TriggerContext):
        match self.trigger_method_name:
            case "pulse":
                self._trigger_pulse()
            case "hold":
                self._trigger_hold()
            case "while_input":
                self._trigger_while_input(context)

    def deactivate(self):
        GPIO.output(self._gpio_pin, GPIO.LOW)
        self.state = "inactive"

    # --- Trigger Methods ---

    def _trigger_pulse(self):
        # pulse all trigger pins
        GPIO.output(self._gpio_pin, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(self._gpio_pin, GPIO.LOW)

    def _trigger_hold(self):
        # hold all trigger pins
        GPIO.output(self._gpio_pin, GPIO.HIGH)
        sleep(self.hold_time)
        GPIO.output(self._gpio_pin, GPIO.LOW)

    def _trigger_while_input(self, context: TriggerContext):
        [trigger_pin, _] = context

        GPIO.output(self._gpio_pin, GPIO.HIGH)

        while GPIO.input(trigger_pin.gpio_pin) == GPIO.HIGH:
            pass

        GPIO.output(self._gpio_pin, GPIO.LOW)
