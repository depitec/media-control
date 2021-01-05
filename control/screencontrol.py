from time import perf_counter, sleep
from threading import Thread, Event
import logging
import pigpio as gpio
from itertools import count
from database import Helper
import sqlite3

db = sqlite3.connect('/home/pi/raspi-room-control/control/control.db')
helper = Helper(db)
log = logging.getLogger('control-main')


class ScreenControl:
    __ids = count(1)

    def __init__(self, open_in_gpio, close_in_gpio, open_out_gpio, close_out_gpio):
        self.id = next(self.__ids)
        self.__SCREEN_OPEN_IN = open_in_gpio
        self.__SCREEN_CLOSE_IN = close_in_gpio
        self.__SCREEN_OPEN_OUT = open_out_gpio
        self.__SCREEN_CLOSE_OUT = close_out_gpio

        self.room_name = helper.get('name-{}'.format(self.id))

        sot_str = helper.get('sot-{}'.format(self.id))
        self.sot = int(sot_str)

        sct_str = helper.get('sct-{}'.format(self.id))
        self.sct = int(sct_str)

        self.is_open = None

        # PI Setup
        self.PI = gpio.pi()

        self.PI.set_mode(self.__SCREEN_OPEN_IN, gpio.INPUT)
        self.PI.set_pull_up_down(self.__SCREEN_OPEN_IN, gpio.PUD_DOWN)
        self.PI.set_mode(self.__SCREEN_CLOSE_IN, gpio.INPUT)
        self.PI.set_pull_up_down(self.__SCREEN_CLOSE_IN, gpio.PUD_DOWN)
        self.PI.set_mode(self.__SCREEN_OPEN_OUT, gpio.OUTPUT)
        self.PI.set_mode(self.__SCREEN_CLOSE_OUT, gpio.OUTPUT)

        self.PI.callback(self.__SCREEN_OPEN_IN, edge=gpio.FALLING_EDGE,
                         func=self.__open_btn_pressed)
        self.PI.callback(self.__SCREEN_CLOSE_IN, edge=gpio.FALLING_EDGE,
                         func=self.__close_btn_pressed)

        self.open_btn = Event()
        self.close_btn = Event()

    def __set_output(self, gpio, time):

        start = perf_counter()
        self.PI.write(gpio, 1)

        while perf_counter() < start + time:
            sleep(0.1)

        self.PI.write(gpio, 0)

    def open_screen(self):
        log.info('[opening] screen in {}'.format(self.room_name))
        self.__set_output(self.__SCREEN_OPEN_OUT, self.sot)
        self.is_open = True
        log.info('[opened] screen in {}'.format(self.room_name))

    def close_screen(self):
        log.info('[closing] screen in {}'.format(self.room_name))
        self.__set_output(self.__SCREEN_CLOSE_OUT, self.sct)
        self.is_open = False
        log.info('[closed] screen in {}'.format(self.room_name))

    def __open_btn_pressed(self, *args):
        if self.PI.read(self.__SCREEN_OPEN_OUT) or self.PI.read(self.__SCREEN_CLOSE_OUT) or self.is_open == True:
            return

        self.open_btn.set()

    def __close_btn_pressed(self, *args):
        if self.PI.read(self.__SCREEN_CLOSE_OUT) or self.PI.read(self.__SCREEN_OPEN_OUT) or self.is_open == False:
            return

        self.close_btn.set()

    def open_btn_handler(self):
        self.open_btn.clear()
        open_screen = Thread(target=self.open_screen)
        open_screen.start()

    def close_btn_handler(self):
        self.close_btn.clear()
        close_screen = Thread(target=self.close_screen)
        close_screen.start()

    def clean_up(self):
        self.PI.write(self.__SCREEN_CLOSE_OUT, 0)
        self.PI.write(self.__SCREEN_CLOSE_IN, 0)
