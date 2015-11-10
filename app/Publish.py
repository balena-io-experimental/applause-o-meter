#!/usr/bin/python

import os, time
from Pubnub import Pubnub

pubKey = os.getenv("PUBLISH_KEY")
subKey = os.getenv("SUBSCRIBE_KEY")
channel = os.getenv("RESIN_DEVICE_UUID")
deviceName = os.getenv("DEV_NAME")
updatePeriod = int(os.getenv("PERIOD"),30)
print('update period is: '+ str(updatePeriod))
pubnub = Pubnub(publish_key=pubKey, subscribe_key=subKey, ssl_on=True)

def publishData(channelName,data):
    message = data
    print message
    # Synchronous pubnub call
    print pubnub.publish(channel=channelName, message=message)

if __name__ == '__main__':
    while True:
        data = time.time()
        print 'publishing : ', data
        publishData(channel,data)
        time.sleep(updatePeriod)
