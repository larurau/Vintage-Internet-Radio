import select
import sys
import time
from neopixel import Neopixel
from machine import Pin
import re
import math
import random

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

current_animation = ""

pixels = Neopixel(1, 0, 28, "GRB")

pixels.brightness(200)

# Regex to match "Color(r, g, b)" pattern
color_pattern = re.compile(r"Color\((\d+),\s*(\d+),\s*(\d+)\)")
# Regex to match "Animation=animation_name" pattern
animation_pattern = re.compile(r"Animation=(\w+)")

# Breathing animation
current_intensity = 255
target_breathing_intensity = 0
target_noise_intensity = 0
min_intensity = 100
max_intensity = 200
max_noise_intensity = 160
breathing_phase = 0
fade_factor = 0.2

# Loop indefinitely
while True:
    poll_results = poll_obj.poll(4)
    if poll_results:
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
            
        match = color_pattern.match(data)
        if match:
            target_red = int(match.group(1))
            target_green = int(match.group(2))
            target_blue = int(match.group(3))
            
        match_animation = animation_pattern.match(data)
        if match_animation:
            current_animation = match_animation.group(1)
            print(f'Current animation is {current_animation}')
            
    else:

        # adjust color

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
            
        # breathing animation
        
        target_breathing_intensity = int((math.sin(breathing_phase) + 1) / 2 * (max_intensity - min_intensity) + min_intensity)
        breathing_phase += 0.01
        if breathing_phase > 2 * math.pi:
                breathing_phase = 0
                
        if current_animation == "breathing":
            if current_intensity < target_breathing_intensity:
                current_intensity += 1
                if current_intensity < target_breathing_intensity:
                    current_intensity += 1
            elif current_intensity > target_breathing_intensity:
                current_intensity -= 1
                if current_intensity > target_breathing_intensity:
                    current_intensity -= 1
        
        # noise animation
                    
        elif current_animation == "noise":
            target_noise_intensity = random.randint(min_intensity, max_noise_intensity)
            current_intensity = int((1 - fade_factor) * current_intensity + fade_factor * target_noise_intensity)
        else:
            current_intensity = 255
            
        new_color = (
            int(current_red * (current_intensity / 255)),
            int(current_green * (current_intensity / 255)),
            int(current_blue * (current_intensity / 255))
        )
        
        # set the LED
        
        pixels.set_pixel(0, new_color)
        pixels.show()
        
        continue
