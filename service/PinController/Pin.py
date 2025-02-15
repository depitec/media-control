from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .PinController import PinController

type PinState = Literal["active", "inactive"]

type PinType = Literal["input", "output"]

type PinTriggerType = Literal["impulse", "hold"]


class Pin:
    controller: PinController
    gpio_pin: int
    state: PinState
    type: PinType
    is_blocked: bool
    trigger_type: PinTriggerType
    trigger_hold_time: int

    def __init__(
        self,
        controller: PinController,  # fixed value never change
        gpio_pin: int,  # fixed value never change
        pin_type: PinType = "input",  # fixed value never change
        trigger_type: PinTriggerType = "impulse",
        trigger_hold_time: int = 5,  # in seconds
        is_blocked: bool = False,
    ):
        self.controller = controller
        self.gpio_pin = gpio_pin
        self.state = "inactive"
        self.type = pin_type
        self.is_blocked = is_blocked
        self.trigger_type = trigger_type
        self.trigger_hold_time = trigger_hold_time
