from time import sleep
from neopixel import Adafruit_NeoPixel, Color

# LED strip configuration:
LED_COUNT      = 64     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
ROW_WIDTH      = 8

def setRowColor(strip, row_number, color):
    start = 0 + row_number*ROW_WIDTH
    end = start + ROW_WIDTH
    for i in range(start, end):
        strip.setPixelColor(i, color)
    strip.show()

def fill_up_to(strip, row, color):
    for i in range(row + 1):
        setRowColor(strip,i,color)

def empty_array(strip):
    for i in range(256):
        strip.setPixelColorRGB(i,0,0,0)
    strip.show()
# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    led_array = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
    led_array.begin()

    while True:
        color = Color(0, 0, 60)

        fill_up_to(led_array,7,color)
        sleep(5)
        empty_array(led_array)
        sleep(3)
