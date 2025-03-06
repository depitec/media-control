from pypjlink import Projector

from typing import TypedDict, Callable, Literal


Trigger_Names = Literal["test_trigger", "pjlink_on", "pjlink_off"]


class __Trigger(TypedDict):
    test_trigger: Callable[[], None]
    pjlink_on: Callable[[str], None]
    pjlink_off: Callable[[str], None]


def __test_trigger():
    print("This is a test trigger")


def __pjlink_on(ip: str):
    with Projector.from_address(ip) as projector:
        projector.authenticate()
        projector.set_power("on")
        projector.close()


def __pjlink_off(ip: str):
    with Projector.from_address(ip) as projector:
        projector.authenticate()
        projector.set_power("off")
        projector.close()


trigger_dict: __Trigger = {
    "test_trigger": __test_trigger,
    "pjlink_on": __pjlink_on,
    "pjlink_off": __pjlink_off,
}
