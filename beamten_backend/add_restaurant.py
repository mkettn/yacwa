#!/usr/bin/env python3
import cgi, re

PRIV_KEY_STORAGE = "/home/yacwa_admin/.ssh/restaurants/"

SSH_CFG_FMT = """
Host {server}
\tHostname {server}
\tUser yacwa
\tPort {port}
\tIdentityFile {id_file}
"""

SSH_CFG_PATH = "/home/yacwa_admin/.ssh/config"

SSH_KEY_CHECK_CMD = "ssh-keygen -y -f {key}"

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
srv = form.getvalue('srv')
priv_key = form['privkey']

print("Content-type:text/html\r\n\r\n")
if not fileitem.filename:
    print("Private Key vergessen!")
    exit()
import shlex, subprocess
args = shlex.split(SSH_KEY_CHECK_CMD.format(key=fileitem.filename))
p = subprocess.Popen(args, shell=False)
rcode = p.wait()
if rcode != 0:
    print("Private Key invalid")
    exit()
# https://wiert.me/2017/08/29/regex-regular-expression-to-match-dns-hostname-or-ip-address-stack-overflow/
# aber mit port zwischen 2 und 5 digits
Valid952HostnameRegex = "^((([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])):([0-9]{2,5})$"
srv_rgx = re.compile(Valid952HostnameRegex)

rslt = srv_rgx.findall(srv)
if not rslt:
    print("server und port vergessen")
    exit()
server = rslt[0]
port = int(rslt[-1])
if port > 2**16 or port < 1024:
    print("port ist außerhalb von (1024, 2^16)")
    exit()

from shutil import move
from os.path import join
priv_id_file = join(PRIV_KEY_STORAGE, f"id_{server}")
move(fileitem.filename, priv_id_file)

new_server = True
with open(SSH_CFG_PATH, "r") as fd:
    for l in fd.readlines():
        if l.find(f"Host {server}") !=-1:
            print("Achtung: Server exisitert bereits, überschreibe keyfile...")
            new_server = False
            break
if new_server:
    ssh_server_config = SSH_CFG_FMT.format(server=server, port=port, id_file=priv_id_file)
    with open(SSH_CFG_PATH, "a") as fd:
        fd.write(ssh_server_config)
print("Restaurant hinzugefügt.")
