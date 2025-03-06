from typing import Dict
import RPi.GPIO as GPIO
from .Pins import PinType, InputPin, OutputPin, VirtualPin
import asyncio


class PinController:
    input_pins: Dict[str, InputPin]
    output_pins: Dict[str, OutputPin]
    virtual_pins: Dict[str, VirtualPin]
    impulse_length: float

    def __init__(self):
        self.impulse_length = 0.1
        self.input_pins = {}
        self.output_pins = {}
        self.virtual_pins = {}

    def register_pin(self, pin_number: int, pin_type: PinType):
        direction = GPIO.OUT if pin_type == "output" else GPIO.IN

        GPIO.setup(pin_number, direction)

        if pin_type == "input":
            input_pin_name = f"I#{len(self.input_pins)}"
            new_input_pin: InputPin = InputPin(self, input_pin_name, pin_number)
            self.input_pins[input_pin_name] = new_input_pin
            GPIO.add_event_detect(
                pin_number,
                GPIO.RISING,
                callback=self.event_rising_edge(new_input_pin),  # type: ignore
            )
            GPIO.add_event_detect(
                pin_number,
                GPIO.FALLING,
                callback=self.event_falling_edge(new_input_pin),  # type: ignore
            )

        if pin_type == "output":
            output_pin_name = f"O#{len(self.input_pins)}"
            new_output_pin: OutputPin = OutputPin(self, output_pin_name, pin_number)
            self.output_pins[output_pin_name] = new_output_pin

    def unregister_pin(self, pin: InputPin | OutputPin):
        if pin.pin_type == "input":
            del self.input_pins[pin.name]
            GPIO.cleanup(pin.gpio_pin)

        if pin.pin_type == "output":
            del self.output_pins[pin.name]
            GPIO.cleanup(pin.gpio_pin)

        if pin.pin_type == "virtual":
            del self.virtual_pins[pin.name]

    def block_pins(self, pins_to_block: list[str]):
        for pin_name in pins_to_block:
            self.input_pins[pin_name].is_blocked = True

    def unblock_pins(self, pins_to_unblock: list[str]):
        for pin_name in pins_to_unblock:
            self.input_pins[pin_name].is_blocked = False

    async def trigger_pins(self, pins: list[str]):
        pins_to_trigger = [self.output_pins[pin_name] for pin_name in pins]

        for pin in pins_to_trigger:
            if pin.trigger_type == "impulse":
                GPIO.output(pin.gpio_pin, GPIO.HIGH)
                await asyncio.sleep(self.impulse_length)
                GPIO.output(pin.gpio_pin, GPIO.LOW)

            if pin.trigger_type == "hold":
                GPIO.output(pin.gpio_pin, GPIO.HIGH)
                await asyncio.sleep(pin.trigger_hold_time)
                GPIO.output(pin.gpio_pin, GPIO.LOW)

            if pin.trigger_type == "while_input":
                GPIO.output(pin.gpio_pin, GPIO.HIGH)

    def event_falling_edge(self, pin: InputPin):
        def callback(channel):
            pin.state = "inactive"

            # unblock pins previously blocked by this pin
            pins_to_block = pin.block_pins
            self.unblock_pins(pins_to_block)

            # block pins previously unblocked by this pin
            pins_to_unblock = pin.unblock_pins
            self.block_pins(pins_to_unblock)

        return callback

    async def event_rising_edge(self, pin: InputPin):
        async def callback(channel):
            pin.state = "active"
            if pin.is_blocked:
                return

            await asyncio.sleep(pin.debounce_time)

            # set pin state to active

            # block pins
            pins_to_block = pin.block_pins
            self.block_pins(pins_to_block)

            # unblock pins
            pins_to_unblock = pin.unblock_pins
            self.unblock_pins(pins_to_unblock)

            # trigger pins
            pins_to_trigger = pin.trigger_pins

            # for pin_name in pins_to_trigger:
            #     await self.__output_trigger(self.output_pins[pin_name])

        return callback
