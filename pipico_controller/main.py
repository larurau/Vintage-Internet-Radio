import select
import sys
import time
from neopixel import Neopixel
from machine import Pin
import re
import math
import random

# Helper functions

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

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

# Regex to match allowed inputs
color_pattern = re.compile(r"Color\((\d+),\s*(\d+),\s*(\d+)\)")
animation_pattern = re.compile(r'Animation\((\w+)\)')
noise_intensity_pattern = re.compile(r'NoiseIntensity\((\d+)\)')
breathing_speed_pattern = re.compile(r'BreathingSpeed\((\d+)\)')

# Animation settings
current_animation = ""
current_intensity = 255
target_breathing_intensity = 0
target_noise_intensity = 0
min_intensity = 100
max_intensity = 200
min_noise_intensity = 20
max_noise_intensity = 230
breathing_phase = 0
noise_intensity = 0.1
breathing_speed = 0.01
rainbow_phase = 0
rainbow_speed = 1

# Loop indefinitely
while True:
    
    # Read input
    
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
            
        color_match = color_pattern.match(data)
        if color_match:
            target_red = int(color_match.group(1))
            target_green = int(color_match.group(2))
            target_blue = int(color_match.group(3))
            
        match_animation = animation_pattern.match(data)
        if match_animation:
            current_animation = match_animation.group(1)
            
        match_noise_intensity = noise_intensity_pattern.match(data)
        if match_noise_intensity:
            noise_intensity = int(match_noise_intensity.group(1))/1000
            
        match_breathing_speed = breathing_speed_pattern.match(data)
        if match_breathing_speed:
            breathing_speed = float(match_breathing_speed.group(1))/1000
      
    # Animate
      
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
        breathing_phase += breathing_speed
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
            target_noise_intensity = random.randint(min_noise_intensity, max_noise_intensity)
            difference = target_noise_intensity - current_intensity
            current_intensity = current_intensity + (difference * noise_intensity)
            
        # special animations
        
        elif current_animation == "special_noise":
            noise_intensity = 1
            current_animation = "noise"
            
        elif current_animation == "rainbow":

            color = wheel(rainbow_phase & 255)
            target_red = color[0]
            target_green = color[1]
            target_blue = color[2]
            
            rainbow_phase += rainbow_speed
            if rainbow_phase > 256:
                rainbow_phase = 0
            
        # default animation
        
        else:
            current_intensity = 255
        
        # set the LED
        
        new_color = (
            int(current_red * (current_intensity / 255)),
            int(current_green * (current_intensity / 255)),
            int(current_blue * (current_intensity / 255))
        )
        
        pixels.set_pixel(0, new_color)
        pixels.show()
        
        continue
