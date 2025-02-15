from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .PinController import PinController

type PinState = Literal["active", "inactive"]

type PinTriggerType = Literal["impulse", "hold"]

type PinType = Literal["input", "output"]


class __Pin:
    controller: PinController
    gpio_pin: int
    pin_type: PinType
    state: PinState
    is_blocked: bool
    unblock_pins: list[int]
    block_pins: list[int]

    def __init__(
        self,
        controller: PinController,  # fixed value never change
        gpio_pin: int,  # fixed value never change
        pin_type: PinType,  # fixed value never change
        is_blocked: bool = False,
        unblock_pins: list[int] = [],
        block_pins: list[int] = [],
    ):
        self.controller = controller
        self.gpio_pin = gpio_pin
        self.state = "inactive"
        self.is_blocked = is_blocked
        self.unblock_pins = unblock_pins
        self.block_pins = block_pins
        self.pin_type = pin_type

    # TODO: add @property and @setter for unblock_pins, block_pins + validation
    def add_unblock_pin(self, pin: int):
        self.unblock_pins.append(pin)

    def add_block_pin(self, pin: int):
        self.block_pins.append(pin)

    def remove_unblock_pin(self, pin: int):
        self.unblock_pins.remove(pin)

    def remove_block_pin(self, pin: int):
        self.block_pins.remove(pin)


type InputCallbacks = Literal["trigger_output", "trigger_pjlink"]


class InputPin(__Pin):
    debounce_time: float
    on_input: InputCallbacks
    pjlink_cmd: str

    # TODO: add pjlink cmd

    def __init__(
        self, controller: PinController, gpio_pin: int, debounce_time: int = 0
    ):
        super().__init__(controller, gpio_pin, "input")
        self.debounce_time = debounce_time


class OutputPin(__Pin):
    trigger_type: PinTriggerType
    trigger_hold_time: float

    def __init__(
        self,
        controller: PinController,
        gpio_pin: int,
        trigger_type: PinTriggerType = "impulse",
        trigger_hold_time: int = 5,
    ):
        super().__init__(controller, gpio_pin, "output")
        self.trigger_type = trigger_type
        self.trigger_hold_time = trigger_hold_time
