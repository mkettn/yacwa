#!/usr/bin/env python3
import cgi, re
from datetime import datetime
REQ_VLIST_HEADER = ["location_srv", "gesundheitsamt", "start", "duration"]
DATE_FMT = "%d-%m-%y-%H:%M"
SSH_CFG_PATH = "/home/yacwa_admin/.ssh/config"
EMAIL_VON_DIESEM_G_AMT = "gesundheitsamt@kaff.de"

# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields
visit_list = form['visit_list']
print("Content-type:text/html\r\n\r\n")
if not visit_list.filename:
    print("Besuchsliste vergessen!")
    exit()

def parse_vlist(fd):
    header = map(str.strip, fd.readline().split(","))
    ret = {}
    if header != REQ_VLIST_HEADER:
        print("Besuchsliste invalid!")
        return -1
    for line, l in enumerate(fd.readlines()):
        line+=1
        ldat = l.split(",")
        srv = ldat[0] # TODO check if valid srv name
        g_amt = ldat[1] # TODO check if valid email
        try:
            start = datetime.strptime(ldat[2].strip(), DATE_FMT)
        except Exception:
            print(f"Datum in L{line}: {ldat[2]} entspricht nicht {DATE_FMT}, überspringe!")
            continue
        try:
            duration = int(ldat[3])
        except Exception:
            print(f"Dauer in L{line}: {ldat[2]} entspricht keine ganzzahl, überspringe!")
            continue
        try:
            ret[g_amt][srv].append(f"{start} {duration}")
        except Exception: # KeyError oder so kann da kommen
            ret[g_amt] = dict()
            ret[g_amt][srv] = []
            ret[g_amt][srv].append(f"{start} {duration}")
    return ret

with open(visit_list.filename, "r") as fd:
    vlist = parse_vlist(fd)

if vlist == -1:
    exit()

import subprocess

def srv_known(srv):
    with open(SSH_CFG_PATH, "r") as fd:
        for l in fd.readlines():
            if l.find(f"Host {server}") !=-1:
                return True
    return False

def send_list(srv, l):
    p = subprocess.Popen(["ssh", srv], stdin=subprocess.PIPE)
    data = "\n".join(l).encode()
    a, b = p.communicate(input=data)
    rcode = p.wait()
    return rcode==0

if EMAIL_VON_DIESEM_G_AMT in vlist.keys():
    for srv, l in ret[EMAIL_VON_DIESEM_G_AMT].items():
        if srv_known(srv):
            send_list(srv, l)
        else:
            print(f"unbekanntes Restaurant: {srv}, überspringe...")
        pass
    del(ret[EMAIL_VON_DIESEM_G_AMT])

# TODO mails an alle anderen Gesundheitsämter versenden!
