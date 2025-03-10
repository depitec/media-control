from __future__ import annotations

from .Pin import Pin
from typing import Union, TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from ..PinManager import TriggerContext
    from .OutputPin import OutputPin
    from .VirtualPin import VirtualPin

type TriggerablePins = Union[OutputPin, VirtualPin]


class InputPin(Pin):
    trigger_pins: list[TriggerablePins]

    def __init__(
        self,
        name: str,
        gpio_pin: int,
    ):
        super().__init__(name, gpio_pin, "input")
        self.trigger_pins = []

    def add_trigger_pin(self, pin: TriggerablePins):
        self.trigger_pins.append(pin)

    def remove_trigger_pin(self, pin: TriggerablePins):
        self.trigger_pins.remove(pin)

    def activate(self, trigger_context: TriggerContext):
        activate_time = datetime.timestamp(datetime.now())
        context = (self, activate_time)

        for pin in self.trigger_pins:
            pin.trigger(context)
