#! /home/pi/.pyenv/shims/python

from time import sleep
from screencontrol import ScreenControl
from beamercontrol import BeamerControl
import signal
import sys
from threading import Thread
import logging


def main_signal_handler(sig, frame):
    logging.info('[shutdown] gracefully shuting down')
    sc1.PI.stop()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, main_signal_handler)
# setup logging
    log = logging.getLogger('control-main')
    logging.basicConfig(filename='/home/pi/logs/control.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',
                        encoding='utf-8', level=logging.DEBUG)

    log.info('[initialize] main loop')

    sc1 = ScreenControl(17, 27, 22, 23)
    bc1 = BeamerControl(24, 25)
    sc2 = ScreenControl(5, 12, 6, 13)
    bc2 = BeamerControl(16, 26,)

    sc1.clean_up()
    sc2.clean_up()
    # main loop
    log.info('[started] main loop')
    while True:
        if sc1.open_btn.is_set():
            sc1.open_btn_handler()

        if sc1.close_btn.is_set():
            sc1.close_btn_handler()

        if sc2.open_btn.is_set():
            sc2.open_btn_handler()

        if sc2.close_btn.is_set():
            sc2.close_btn_handler()

        sleep(0.1)
