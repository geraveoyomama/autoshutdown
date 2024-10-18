#!/usr/bin/python3
import os,time
from subprocess import getoutput
import datetime

#Network interface to monitor ("ip a" to list the available devices) Leave empty for autoconfig.
INTERFACE = ''
#Maximum speed to reset the collected data
OVERRIDE_SPEED = 100
#Minimum speed in KB/s that must be achieved
MIN_SPEED = 4
#Number of samples to calculate average speed
SAMPLES = 1200 #1200 was 10
#Set the interval in seconds between samples (note that number of samples*interval is the minimum time for shutdown)
INTERVAL = 0 #0 disables was 0
#Sleep the script so that it doesnt shut down instantly
STARTWAIT = 0 #0 disables

#def who ():
#    return bool(getoutput("who"))
#def sampleexceed ():
#    return (len(network) >= SAMPLES)
#def avgspeed ():
#    return (sum(network)/len(network) < MIN_SPEED)

def worker ():
    time.sleep(STARTWAIT)
    network = []

    if bool(INTERFACE) is True:
      PROBE = INTERFACE
    else:
      PROBE = getoutput("ip -o -4 route show to default | awk '{print $5}'")
    while True:
      SPEED = int(float(getoutput("ifstat -i %s 1 1 | awk '{print $1+$2}' | sed -n '3p'" % PROBE)))
      #Resets the list in case of last minute high load.

      if SPEED >= OVERRIDE_SPEED:
        network = []
      else:
        network.insert(0,SPEED)
        print(network)
        if len(network) >= (SAMPLES + 1):
          network.pop()
        if (len(network) >= SAMPLES) and (sum(network)/len(network)) < MIN_SPEED and bool(getoutput('who')) is False:
          os.system('sudo shutdown')
          #os.system("shutdown --halt +5 “Attention. The system is going down in five minutes.")
          exit()  # if shutdown is activated, then exit script

      #now = datetime.datetime.now()
      #print(now.strftime('%d-%m-%Y %H:%M:%S'), network)
      time.sleep(INTERVAL)

worker()
