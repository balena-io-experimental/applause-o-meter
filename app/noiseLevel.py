import os
import signal
import sys
import time

import audioop
import pyaudio
from pubnub import Pubnub

from Led_Array import Led_Array, Color

AUDIO_VOLUME = float(os.getenv('AUDIO_VOLUME', 1.0))
RESIN_DEVICE_UUID = os.getenv("RESIN_DEVICE_UUID")

PUBNUB_ENABLE = os.getenv("PUBNUB_ENABLE", "off")
PUBLISH_KEY = os.getenv("PUBLISH_KEY")
SUBSCRIBE_KEY = os.getenv("SUBSCRIBE_KEY")

RATE = 44100
FORMAT = pyaudio.paInt16
AUDIO_MAX = 2 ** 15
CHANNELS = 2

MAX_ROWS = 32

RED = Color(100, 0, 0)
BLUE = Color(0, 0, 160)

pubnub = Pubnub(publish_key=PUBLISH_KEY,
                subscribe_key=SUBSCRIBE_KEY, ssl_on=True)

p = pyaudio.PyAudio()
led_array = Led_Array()

current_max = 0
current_level = 0

count = 0

def audio_callback(in_data, frame_count, time_info, status):
    global current_max
    global current_level
    global count
    count += 1

    # audio rms power value
    rms = audioop.rms(in_data, 2) * AUDIO_VOLUME

    # current_level is 0-32 value shown on LEDs
    current_level = min(int(rms * MAX_ROWS / AUDIO_MAX), MAX_ROWS)
    current_max = min(max(current_level, current_max), MAX_ROWS)

    led_array.empty_array()
    led_array.setRowColor(current_max, RED)
    led_array.fill_up_to(current_level, BLUE)
    led_array.render()

    return (None, pyaudio.paContinue)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                frames_per_buffer=RATE / 10,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=audio_callback)


def clean_up():
    print 'Clean up streams and pyaudio'
    stream.stop_stream()
    stream.close()
    p.terminate()


def handler(signal, frame):
    clean_up()
    print 'exiting python process'
    sys.exit(0)

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

stream.start_stream()

while stream.is_active():
    if PUBNUB_ENABLE == "on":
        message = {'current_max': current_max, 'current_level': current_level}
        print 'pubnub: ', message
        pubnub.publish(RESIN_DEVICE_UUID, message)

    print "audio callback rate: %dHz" % count
    count = 0

    time.sleep(1)

clean_up()
