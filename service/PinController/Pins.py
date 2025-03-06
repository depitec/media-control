from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from .Trigger import Trigger_Names, trigger_dict

if TYPE_CHECKING:
    from .PinController import PinController

type PinState = Literal["active", "inactive"]

type OutputPinTriggerType = Literal["pulse", "hold", "while_input"]

type PinType = Literal["input", "output", "virtual"]


class __Pin:
    controller: PinController
    gpio_pin: int
    name: str
    pin_type: PinType
    state: PinState
    is_blocked: bool
    unblock_pins: list[str]
    block_pins: list[str]

    def __init__(
        self,
        controller: PinController,
        name: str,
        gpio_pin: int,  # fixed value never change
        pin_type: PinType,  # fixed value never change
        is_blocked: bool = False,
        unblock_pins: list[str] = [],
        block_pins: list[str] = [],
    ):
        self.controller = controller
        self.name = name
        self.gpio_pin = gpio_pin
        self.pin_type = pin_type
        self.state = "inactive"
        self.is_blocked = is_blocked
        self.unblock_pins = unblock_pins
        self.block_pins = block_pins

    # TODO: add @property and @setter for unblock_pins, block_pins + validation
    def add_unblock_pin(self, pin_name: str):
        self.unblock_pins.append(pin_name)

    def add_block_pin(self, pin_name: str):
        self.block_pins.append(pin_name)

    def remove_unblock_pin(self, pin_name: str):
        self.unblock_pins.remove(pin_name)

    def remove_block_pin(self, pin_name: str):
        self.block_pins.remove(pin_name)


class InputPin(__Pin):
    debounce_time: float
    trigger_pins: list[str]

    def __init__(
        self,
        controller: PinController,
        name: str,
        gpio_pin: int,
        debounce_time: int = 0,
    ):
        super().__init__(controller, name, gpio_pin, "input")
        self.debounce_time = debounce_time

    def add_trigger_pin(self, pin_name: str):
        self.trigger_pins.append(pin_name)

    def remove_trigger_pin(self, pin_name: str):
        self.trigger_pins.remove(pin_name)


class OutputPin(__Pin):
    trigger_type: OutputPinTriggerType
    trigger_hold_time: float

    def __init__(
        self,
        controller: PinController,
        name: str,
        gpio_pin: int,
        trigger_type: OutputPinTriggerType = "pulse",
        trigger_hold_time: int = 5,
    ):
        super().__init__(controller, name, gpio_pin, "output")
        self.trigger_type = trigger_type
        self.trigger_hold_time = trigger_hold_time


class VirtualPin(__Pin):
    trigger_fn: Trigger_Names
    pin_adress: str

    def __init__(
        self,
        controller: PinController,
        name: str,
        pin_adress: str,
        trigger_fn: Trigger_Names,
    ):
        super().__init__(controller, name, -1, "virtual")

        # check if trigger_fn is in trigger dict
        if trigger_fn not in trigger_dict:
            raise ValueError(f"Trigger: {trigger_fn} function not found")
        else:
            self.trigger_fn = trigger_fn

        self.pin_adress = pin_adress

    def trigger(self):
        if self.trigger_fn == "test_trigger":
            trigger_dict[self.trigger_fn]()
            return

        trigger_dict[self.trigger_fn](self.pin_adress)
