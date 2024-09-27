import select
import sys
import time
from neopixel import Neopixel
from machine import Pin

# Startup
led_onboard = Pin(25, Pin.OUT)
led_onboard.on()
time.sleep(2)
led_onboard.off()

# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# Set up led
current_red = 0
current_green = 0
current_blue = 0

target_red = 0
target_green = 0
target_blue = 0

pixels = Neopixel(1, 0, 28, "GRB")

pixels.brightness(200)

# Loop indefinitely
while True:
    # Wait for input on stdin
    poll_results = poll_obj.poll(5) # the '1' is how long it will wait for message before looping again (in microseconds)
    if poll_results:
        # Read the data from stdin (read data coming from PC)
        data = sys.stdin.readline().strip()
        
        if data == "red":
            target_red = 255
            target_green = 0
            target_blue = 0
        if data == "green":
            target_red = 0
            target_green = 255
            target_blue = 0
        if data == "blue":
            target_red = 0
            target_green = 0
            target_blue = 255
            
        # Write the data to the input file
        sys.stdout.write("received data: " + data + "\r")
    else:
        # do something if no message received (like feed a watchdog timer)
        if current_red < target_red:
            current_red += 1
        elif current_red > target_red:
            current_red -= 1
            
        if current_green < target_green:
            current_green += 1
        elif current_green > target_green:
            current_green -= 1
            
        if current_blue < target_blue:
            current_blue += 1
        elif current_blue > target_blue:
            current_blue -= 1
            
        new_color = (current_red, current_green, current_blue)
        pixels.set_pixel(0, new_color)
        pixels.show()
        
        continue
