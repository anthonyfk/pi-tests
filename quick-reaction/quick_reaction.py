#!/usr/bin/env python3

from RPi import GPIO

import time



def main():
    # Initialize the GPIO module.
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    print("something")


if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()

