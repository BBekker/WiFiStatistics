import sys
import os
import time

channels = sys.argv[1:]
counter =0
while True:
    counter += 1
    counter = counter % (len(sys.argv)-1)
    os.system("iwconfig wlan0mon channel "+channels[counter])
    print("channel "+channels[counter])
    time.sleep(5)


