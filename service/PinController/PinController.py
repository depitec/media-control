import RPi.GPIO as GPIO
from .Pin import PinType, InputPin, OutputPin
import asyncio


class PinController:
    input_pins: list[InputPin]
    output_pins: list[OutputPin]
    impulse_length: float

    def __init__(self):
        self.output_pins = []
        self.input_pins = []
        self.impulse_length = 0.1

    def register_pin(self, pin_number: int, pin_type: PinType):
        direction = GPIO.OUT if pin_type == "output" else GPIO.IN

        GPIO.setup(pin_number, direction)

        if pin_type == "input":
            newInputPin: InputPin = InputPin(self, pin_number)
            self.input_pins.append(newInputPin)

        if pin_type == "output":
            newOutputPin: OutputPin = OutputPin(self, pin_number)
            self.output_pins.append(newOutputPin)

    def unregister_pin(self, pin_number: int, pin_type: PinType):
        GPIO.cleanup(pin_number)
        if pin_type == "input":
            self.input_pins = [
                item for item in self.input_pins if item.gpio_pin != pin_number
            ]

        if pin_type == "output":
            self.output_pins = [
                item for item in self.output_pins if item.gpio_pin != pin_number
            ]

    def find_output_pin(self, pin_number: int):
        pin = next(
            (item for item in self.output_pins if item.gpio_pin == pin_number), None
        )
        # TODO: Add error handling if pin is not found
        return pin

    def trigger_pin(self, pin_number: int):
        pin = self.find_output_pin(pin_number)
        # TODO: Add error handling
        if pin is None:
            return

        if pin.trigger_type == "impulse":
            asyncio.run(self.__trigger_impulse(pin))

        if pin.trigger_type == "hold":
            asyncio.run(self.__trigger_hold(pin))

    async def __trigger_impulse(self, pin: OutputPin):
        GPIO.output(pin.gpio_pin, GPIO.HIGH)
        await asyncio.sleep(self.impulse_length)
        GPIO.output(pin.gpio_pin, GPIO.LOW)

    async def __trigger_hold(self, pin: OutputPin):
        GPIO.output(pin.gpio_pin, GPIO.HIGH)
        await asyncio.sleep(pin.trigger_hold_time)
        GPIO.output(pin.gpio_pin, GPIO.LOW)

    async def add_input_event_detect(self, pin: InputPin):
        async def callback(channel):
            if pin.is_blocked:
                return

            pin.state = "active"

            await asyncio.sleep(pin.debounce_time)

        GPIO.add_event_detect(pin.gpio_pin, GPIO.RISING, callback=callback)
