#!/usr/bin/python

import os, time
from pubnub import Pubnub

pubKey = os.getenv("PUBLISH_KEY")
subKey = os.getenv("SUBSCRIBE_KEY")
channel = os.getenv("RESIN_DEVICE_UUID")

pubnub = Pubnub(publish_key=pubKey, subscribe_key=subKey, ssl_on=True)

def publishData(channelName,message):
    print 'from pub func: ' ,message
    # Synchronous pubnub call
    print pubnub.publish(channel=channelName, message=message)

if __name__ == '__main__':
    number = 0
    while True:
        data = {
            'current_level': number
        }
        print 'publishing : ', data
        publishData(channel,data)
        number = number + 1
        time.sleep(60)
