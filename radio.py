import datetime
import signal
import sys

import outputHandling
from inputHandling import MouseDevice
from outputHandling import Channel, FilePlayer

# methods

def calculate_position(change, previous_position, max_value):
    new_position = previous_position + change

    if new_position > max_value:
        new_position -= max_value
    elif new_position < 0:
        new_position = max_value + previous_position

    return new_position

# setup

client1 = Channel(
    500,
    50,
    400,
    "https://cast1.torontocast.com:2170/;.mp3",
    6600)
background_noise = FilePlayer(
    'noise.mp3',
    6601)

mouse = MouseDevice(1133, 49256)

position = 1000
position_max_value = 2000
last_second = datetime.datetime.now().second
velocity = 0

# signal handling

def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!\n')
    outputHandling.close_player(client1)
    outputHandling.close_player(background_noise)
    mouse.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# execution

print("\nStarting loop ...")
while True:

    position = calculate_position(velocity, position, position_max_value)

    if last_second != datetime.datetime.now().second:
        print("position: " + str(position))
        last_second = datetime.datetime.now().second

    client_volume = client1.set_volume_based_on_position(position)
    background_noise.set_volume(100-client_volume)

    velocity = mouse.read_movement() / 3