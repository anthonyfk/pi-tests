#!/usr/bin/env python3

from collections import defaultdict
from RPi import GPIO

import time
import random


# Define our pins.
class Pin(object):
    LED = 4
    BUTTON_A = 14
    BUTTON_B = 15


class QuickReact(object):

    def __init__(self):
        self.scores = defaultdict(int)
        self.times = defaultdict(list)

    def init_GPIO(self):
        print("Initializing GPIO ...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(Pin.LED, GPIO.OUT)
        GPIO.setup(Pin.BUTTON_A, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(Pin.BUTTON_B, GPIO.IN, GPIO.PUD_UP)

    def go(self):
        # Blink light.
        GPIO.output(Pin.LED, 1)
        time.sleep(random.uniform(5, 10))
        GPIO.output(Pin.LED, 0)

        # Detect button.
        # TODO


def main():
    qr = QuickReact()
    qr.init_GPIO()
    qr.go()


if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
