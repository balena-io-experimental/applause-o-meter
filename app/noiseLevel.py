import pyaudio
import audioop
import signal
import sys, os
from time import sleep

from Led_Array import Led_Array, Color

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
AUDIO_MAX = int(os.getenv('AUDIOMAX','20000'))
print AUDIO_MAX

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

current_max = -100000

if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    led_array = Led_Array()

    while True:
        try:
            data_chunk = stream.read(CHUNK)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            continue

        rms = audioop.rms(data_chunk, 2)
        if rms > current_max:
            current_max = rms
        level = convert_scale(rms, 0, AUDIO_MAX, 0, MAX_ROWS)
        max_level = convert_scale(current_max, 0, AUDIO_MAX, 0, MAX_ROWS)

        led_array.empty_array()
        red = Color(100,0,0)
        led_array.setRowColor(int(max_level),red)
        blue = Color(0, 0, 100)
        led_array.fill_up_to(int(level),blue)
        led_array.render()
        sleep(0.05)

clean_up()
