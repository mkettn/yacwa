#!/usr/bin/env python3

CORONA_FILE="/var/www/html/corona.txt"
#CORONA_FILE="./corona.txt"
date_fmt="%d-%m-%y-%H:%M"

from datetime import datetime

print("Hello Beamter, what do you want?")
print("(0) append data to corona file")
print("(1) ping")

def append():
    # TODO check if start is a valid UTC timestamp
    start = input(f"enter start date+time ({date_fmt}):")
    try:
        start = datetime.strptime(start, date_fmt)
    except Exception:
        print("wrong format")
    duration = int(input("enter duration in minutes:"))
    with open(CORONA_FILE, "a") as fd:
        print(start.strftime(date_fmt), duration, file=fd)
    print("current state:")
    with open(CORONA_FILE, "r") as fd:
        print(*fd.readlines(), sep='', end='')
    print("thank you!")

def pong():
    print("pong")

{'0': append,
 '1': pong
}.get(input(), pong)()
