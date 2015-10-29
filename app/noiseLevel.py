import pyaudio
import audioop
import signal
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1
AUDIO_MAX = 20000

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
for i in range(0, int(RATE / CHUNK * 5)):
    data_chunk = stream.read(CHUNK)
    rms = audioop.rms(data_chunk, 2)
    if rms > current_max:
        current_max = rms
    level = convert_scale(rms, 0, AUDIO_MAX, 0, MAX_ROWS)
    max_level = convert_scale(current_max, 0, AUDIO_MAX, 0, 32)
    print 'level: ', level, 'current max: ', max_level

clean_up()
