import time
print 'hello from python, i just synced at '+ str(time.time())

from Led_Array import Led_Array, Color

if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    led_array = Led_Array()

    while True:
        color = Color(0, 60, 0)
        led_array.fill_up_to(7,color)
        time.sleep(5)
        led_array.empty_array()
        time.sleep(3)
