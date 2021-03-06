import os
import subprocess
import platform
import random
from time import sleep
fake=True
if platform.machine() == 'armv7l':
    from Adafruit_LED_Backpack import SevenSegment
    d1 = SevenSegment.SevenSegment(address=0x70)
    d2 = SevenSegment.SevenSegment(address=0x72)
    d3 = SevenSegment.SevenSegment(address=0x71)
    displays = [d1,d2,d3]
    assume_i2cdisplay = True # naive but ok for now.
    my_ip = subprocess.check_output(['hostname','-I']).rstrip()
else:
    assume_i2cdisplay = False
    displays = ["d1","d2","d3"]
    my_ip = "000.000.000.000"

counter = 0


def ping(host):
    is_up = False
    if fake:
        sleep(random.uniform(5.0,15.0)/1000.0)
        is_up = True
    else:
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

def display_str(str,displays):
    numstr = "%12s          " % str
    dc = 0
    for d in displays:
        for i in range(dc+4,dc,-1):
            if assume_i2cdisplay:
                d.set_digit(i-dc,numstr[i])
            else:
                print("display %s, digit %d = %d : %s" % (d,i,i-dc,numstr[i]))
        if assume_i2cdisplay:
            d.write_display()
        dc = dc+4

def display_num4(num,displays):
    numstr = " %12d" % num
    display_str(numstr,displays)


display_str(my_ip,displays)
sleep(20)
while (True):
    if ping("192.168.0.1"):
        counter = counter +1
    display_num4(counter,displays)
