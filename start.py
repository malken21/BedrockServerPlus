import subprocess
from subprocess import PIPE

import server_plus.util as util

config = util.readJSON("server_plus/config.json")

cmd = config["startCMD"]

test = 0

proc = subprocess.Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE)
while proc.poll() is None:
    for line in proc.stdout:
        print(line.decode(), end="")

