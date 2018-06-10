import os
import subprocess
counter = 0

def ping(host):
    is_up = False
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', '-c', '1','-W','1','-n',host],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            is_up = True
        except subprocess.CalledProcessError:
                is_up = False
    return is_up

def display_num4(num,displays):
    numstr = "%12d" % num
    dc = 0
    for d in displays:
        for i in range(dc,dc+4):
            print("display %s, digit %d : %s" % (d,i,numstr[i]))
        dc = dc+4

while (True):
    if ping("192.168.0.1"):
        counter = counter +1
    display_num4(counter,["d1","d2","d3"])
