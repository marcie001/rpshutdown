#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import os
import time

# 入力のピンの番号
bcm = int(os.getenv('BCM', '13'))

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup(bcm)

GPIO.setup(bcm, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 関数定義
cnt = 0
SHUTDOWN_CNT = 30

def button_down(ch):
    global cnt
    cnt = 1

    while GPIO.input(bcm) == GPIO.LOW:
        cnt += 1
        if cnt > SHUTDOWN_CNT:
            os.system("sudo shutdown -h now > /dev/null 2>&1")
            exit(0)
        time.sleep(0.1)

    if cnt <= SHUTDOWN_CNT:
        os.system("sudo shutdown -r now > /dev/null 2>&1")
        exit(0)

GPIO.add_event_detect(bcm, GPIO.FALLING, callback = button_down, bouncetime = 500)

while True:
    time.sleep(1)
