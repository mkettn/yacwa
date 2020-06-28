#!/usr/bin/env python3

#CORONA_FILE="/var/www/html/corona.txt"
CORONA_FILE="./corona.txt"
date_fmt="%d-%m-%y-%H:%M"

from datetime import datetime
from sys import stdin

print("Enter new stuff:")

with open(CORONA_FILE, "a") as fd:
    for l in stdin.readlines():
        try:
            start, duration = l.split()
            start = datetime.strptime(start, date_fmt)
            duration = int(duration)
        except Exception:
            continue
        print(start.strftime(date_fmt), duration, file=fd)
