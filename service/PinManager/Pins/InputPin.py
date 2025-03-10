from __future__ import annotations

from .Pin import Pin
from typing import Union, TYPE_CHECKING
from time import sleep
from datetime import datetime


if TYPE_CHECKING:
    from ..PinManager import TriggerContext
    from .OutputPin import OutputPin
    from .VirtualPin import VirtualPin

type TriggerablePins = Union[OutputPin, VirtualPin]


class InputPin(Pin):
    trigger_pins: list[TriggerablePins]
    trigger_delay: float  ## Time in seconds to wait before triggering the output pin

    def __init__(
        self,
        name: str,
        gpio_pin: int,
    ):
        super().__init__(name, gpio_pin, "input")
        self.trigger_pins = []
        self.trigger_delay = 0

    def add_trigger_pin(self, pin: TriggerablePins):
        self.trigger_pins.append(pin)

    def remove_trigger_pin(self, pin: TriggerablePins):
        self.trigger_pins.remove(pin)

    def activate(self, trigger_context: TriggerContext):
        self.state = "active"

        activate_time = datetime.timestamp(datetime.now())
        context = (self, activate_time)

        sleep(self.trigger_delay)

        for pin in self.trigger_pins:
            pin.trigger(context)
