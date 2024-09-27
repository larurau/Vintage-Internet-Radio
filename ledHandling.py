import argparse
import os
import random
import sys
import time
from rpi_ws281x import PixelStrip, Color
import config

# Locking

def check_and_create_lock():
    if os.path.exists(config.LED_LOCKFILE):
        print("Another instance is using the LED strip. Exiting...")
        sys.exit(1)
    else:
        with open(config.LED_LOCKFILE, "w") as f:
            f.write(str(os.getpid()))

def remove_lock():
    if os.path.exists(config.LED_LOCKFILE):
        os.remove(config.LED_LOCKFILE)

# Radio specific effects

def startup_animation(strip, min_brightness=0, max_brightness=255, step=5, wait_ms=20):

    # Fade in effect
    for brightness in range(min_brightness, max_brightness + 1, step):
        color = Color(0, brightness, 0)  # White fade-in
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)  # Adjust fade-in speed with wait_ms

def breathe_animation(strip, min_intensity=150, max_intensity=200, step=2, wait_ms=50):
    # Breathe in (increase brightness)
    for brightness in range(min_intensity, max_intensity, step):
        color = Color(0, brightness, 0)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

    # Breathe out (decrease brightness)
    for brightness in range(max_intensity, min_intensity, -step):
        color = Color(0, brightness, 0)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def noise_animation(strip, wait_ms=50, fade_factor=0.1):
    """Simulate smoother static noise effect with gradual transitions."""
    current_brightness = [0] * strip.numPixels()  # Keep track of brightness per pixel

    for _ in range(100):  # Run effect for 100 cycles
        for i in range(strip.numPixels()):
            # Generate a target brightness randomly between 0 and 255
            target_brightness = random.randint(0, 255)

            # Gradually move current brightness towards target brightness
            current_brightness[i] = int((1 - fade_factor) * current_brightness[i] + fade_factor * target_brightness)

            # Apply the updated brightness to the pixel
            strip.setPixelColor(i, Color(0, current_brightness[i], 0))  # Green channel

        strip.show()
        time.sleep(wait_ms / 1000.0)

# Basic colors

def red_color_animation(strip, wait_ms=10, iterations=1):

    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255, 30, 30))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def green_color_animation(strip, wait_ms=10, iterations=1):

    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(30, 255, 30))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def blue_color_animation(strip, wait_ms=10, iterations=1):

    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(30, 30, 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def reset_colors(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

# Testing

def test_colors(strip):
    print('Red color')
    red_color_animation(strip)
    print('Green color')
    green_color_animation(strip)
    print('Blue color')
    blue_color_animation(strip)

def test_radio_effects(strip):
    print('Startup')
    startup_animation(strip)
    print('Noise color')
    noise_animation(strip)
    print('Breathe')
    breathe_animation(strip)

def test_led(test_method):

    pixel_strip = PixelStrip(config.LED_COUNT, config.LED_PIN, config.LED_FREQ_HZ, config.LED_DMA, config.LED_INVERT, config.LED_BRIGHTNESS, config.LED_CHANNEL)
    pixel_strip.begin()

    try:
        while True:
            if test_method == 'colors':
                test_colors(pixel_strip)
            elif test_method == 'radio':
                test_radio_effects(pixel_strip)

    except KeyboardInterrupt:
        reset_colors(pixel_strip, Color(0, 0, 0), 10)  # Clear LEDs on exit

if __name__ == "__main__":

    try:
        check_and_create_lock()

        parser = argparse.ArgumentParser(description='Select which test to run.')
        parser.add_argument('test', choices=['colors', 'radio'], help='Choose which test to run')

        args = parser.parse_args()

        test_led(args.test)
    finally:
        remove_lock()