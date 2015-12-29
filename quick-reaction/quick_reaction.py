#!/usr/bin/env python3

from collections import defaultdict
from RPi import GPIO

import time
import random
import threading


# Define our pins.
class Pin(object):
    LED = 4
    BUTTON_A = 14
    BUTTON_B = 15


class QuickReact(object):

    def __init__(self):
        self.scores = defaultdict(int)
        self.times = defaultdict(list)

        self.button_condition = threading.Condition()
        self.button_pusher = None

        self.can_push = False
        self.light_off_time = None
        self.button_pushed_time = None

        self.names = {}

    def set_names(self):
        self.names[Pin.BUTTON_A] = input('Player 1: ')
        self.names[Pin.BUTTON_B] = input('Player 2: ')

    def init_GPIO(self):
        print("Initializing GPIO ...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(Pin.LED, GPIO.OUT)
        GPIO.setup(Pin.BUTTON_A, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(Pin.BUTTON_B, GPIO.IN, GPIO.PUD_UP)

        GPIO.add_event_detect(Pin.BUTTON_A, GPIO.RISING, callback=self.on_button_press)
        GPIO.add_event_detect(Pin.BUTTON_B, GPIO.RISING, callback=self.on_button_press)

    def on_button_press(self, pin):
        if not self.can_push:
            print("%s pushed too soon!" % self.names[pin])
            return

        with self.button_condition:
            if self.button_pusher is None:
                print("%s pushed first!" % self.names[pin])
                self.button_pusher = pin
                self.button_pushed_time = time.time()
                self.button_condition.notify_all()
            else:
                print("%s pushed too late!" % self.names[pin])

    def go(self):
        for i in range(5):
            print("\nRound %d ..." % (i+1))

            # Blink light.
            GPIO.output(Pin.LED, 1)
            time.sleep(random.uniform(5, 10))
            self.can_push = True
            self.light_off_time = time.time()
            GPIO.output(Pin.LED, 0)

            # Wait for button.
            print("Waiting for button press ...")
            with self.button_condition:
                self.button_condition.wait()

            winner = self.button_pusher
            self.button_pusher = None
            self.can_push = False

            self.scores[winner] += 1
            self.times[winner].append(self.button_pushed_time - self.light_off_time)
            print("%s won after: %.2f seconds" % (self.names[winner], self.button_pushed_time-self.light_off_time))

        print("\nScore:")
        for pin, score in sorted(self.scores.items(), key=lambda x: x[1]):
            print("%s: %d" % (self.names[pin], score))


def main():
    qr = QuickReact()
    qr.init_GPIO()
    qr.set_names()
    qr.go()


if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
