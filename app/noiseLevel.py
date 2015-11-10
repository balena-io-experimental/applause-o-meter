import pyaudio
import audioop
import signal
import sys, os
import time
from pubnub import Pubnub

from Led_Array import Led_Array, Color

#set up pubnub object
pubKey = os.getenv("PUBLISH_KEY")
subKey = os.getenv("SUBSCRIBE_KEY")
channel = os.getenv("RESIN_DEVICE_UUID")
pubnub = Pubnub(publish_key=pubKey, subscribe_key=subKey, ssl_on=True)
publish_enable = os.getenv("PUB_ENABLE","off")
print publish_enable

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
AUDIO_MAX = int(os.getenv('AUDIOMAX','20000'))
print 'AUDIO_Max = ',AUDIO_MAX
MAX_ROWS = 8

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
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

def convert_scale(noise_level, input_min, input_max, output_min, output_max):
    input_span = input_max - input_min
    output_span = output_max - output_min

    value_scaled = float(noise_level - input_min) / float(input_span)

    return output_min + (value_scaled * output_span)

def pubnub_callback(message):
    print('publishing : ', message)

current_max = -100000
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    led_array = Led_Array()
    loop_count = 0
    while True:
        start_time = time.time()
        try:
            data_chunk = stream.read(CHUNK)
        except IOError as e:
            # print "I/O error({0}): {1}".format(e.errno, e.strerror)
            continue

        #audio rms power value
        rms = audioop.rms(data_chunk, 2)
        #current_level is 0-32 value shown on LEDs
        current_level = int(convert_scale(rms, 0, AUDIO_MAX, 0, MAX_ROWS))

        if current_level > current_max:
            current_max = current_level
            #check if we go over the limit, then set to 32.
            if current_max > 32:
                current_max = 32

            print 'Current Max is: ',current_max
        loop_count = loop_count + 1

        if loop_count >=15:
            message = {'current_max': current_max, 'current_level': current_level}
            if publish_enable == "on":
                pubnub.publish(channel,message,callback=pubnub_callback, error=pubnub_callback)

            if current_max <= 1:
                current_max = 1
            else:
                # if it been a while, then receed the max a bit.
                current_max = current_max - 1
                loop_count = 0

        led_array.empty_array()
        red = Color(100,0,0)
        led_array.setRowColor(current_max,red)
        blue = Color(0, 0, 160)
        led_array.fill_up_to(current_level,blue)
        led_array.render()

        # sleep(0.15)
        # print("--- %s seconds ---" % (time.time() - start_time))
clean_up()
