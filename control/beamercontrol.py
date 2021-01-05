import logging
import pigpio as gpio
from itertools import count
from pypjlink import Projector
from database import Database

log = logging.getLogger('control-main')

class BeamerControl:
    __ids = count(1)

    def __init__(self, gpio_on, gpio_off, port=4352, timeout=10):
        self.db = Database()
        self.id = next(self.__ids)

        self.ip = self.db.get('ip-{}'.format(self.id))
        try:
            self.projector = Projector.from_address(
                self.ip, 4352, timeout=timeout)
        except Exception:
            log.warning(
                "[error] can't connect with projector {}, ip: {}".format(self.id, self.ip))
            self.projector = None

        self.room_name = self.db.get('name-{}'.format(self.id))

        self.PI = gpio.pi()
        self.PI.set_mode(gpio_on, gpio.INPUT)
        self.PI.set_mode(gpio_off, gpio.INPUT)

        self.PI.callback(gpio_on, gpio.FALLING_EDGE, self.on)
        self.PI.callback(gpio_off, gpio.FALLING_EDGE, self.off)

    def on(self, *args):
        if self.projector == None:
            return
        log.info('[on] beamer in {}'.format(self.room_name))
        self.projector.authenticate()
        self.projector.set_power('on')

    def off(self, *args):
        if self.projector == None:
            return
        log.info('[off] beamer in {}'.format(self.room_name))
        self.projector.authenticate()
        self.projector.set_power('off')
