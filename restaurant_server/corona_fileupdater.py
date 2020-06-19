#!/usr/bin/env python3
CORONA_FILE="/var/www/html/corona.txt"
#CORONA_FILE="./corona.txt"

max_keep_in_days = 14
date_fmt="%d-%m-%y-%H:%M"

from datetime import datetime, timedelta

now = datetime.now()
too_old = now - timedelta(days=max_keep_in_days)

def timefi(l):
    start, duration = l.split(' ')
    start = datetime.strptime(start, date_fmt)
#    return false if too old
    return start > too_old

with open(CORONA_FILE) as fd:
    still_valid = filter(timefi, fd.readlines())

with open(CORONA_FILE, "w") as fd:
    print(*still_valid, file=fd)
