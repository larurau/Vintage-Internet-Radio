import datetime
import signal
import sys
import random

import config
import outputHandling
from dataManagement import ChannelConfig
from inputHandling import MouseDevice
from outputHandling import InternetRadioPlayer, FilePlayer

# methods

def calculate_position(change, previous_position, max_value):
    new_position = previous_position + change

    if new_position > max_value:
        new_position -= max_value
    elif new_position < 0:
        new_position = max_value + previous_position

    return new_position

def find_closest_channel(current_position, channels):
    calculated_channel = None
    min_distance = float('inf')  # Start with a large number

    for channel in channels:
        distance = abs(current_position - channel.position)
        if distance < min_distance:
            min_distance = distance
            calculated_channel = channel

    return calculated_channel

def calculate_channel_positions(channels, extra_distance=50):

    initial_position = 0
    current_position = initial_position

    print(f"\nInitialise channel positions:")

    for index, channel in enumerate(channels):

        # space necessary "below"
        current_position += channel.perception_range

        channel.position = current_position
        print(f"Initialised \"{channel.name}\" at position {current_position}")

        # space necessary "above" as well as extra distance
        current_position += channel.perception_range + extra_distance

    print("Finished calculating channel positions")
    print(f"Maximum position is {current_position}\n")
    return channels, current_position

# setup

mouse = MouseDevice(config.MOUSE_VENDOR_ID, config.MOUSE_PRODUCT_ID)

channel_list = [ChannelConfig(**channel) for channel in config.CHANNEL_LIST]
channel_list, position_max_value = calculate_channel_positions(channel_list)

position = config.INITIAL_POSITION
if config.INITIAL_POSITION_RANDOM:
    position = random.randint(0, position_max_value)
last_second = datetime.datetime.now().second
velocity = 0

closest_channel = find_closest_channel(position, channel_list)

channel_player = InternetRadioPlayer(
    closest_channel,
    config.MPD_PORT_1)
background_noise = FilePlayer(
    'noise.mp3',
    config.MPD_PORT_2)

# signal handling

def signal_handler(_sig, _frame):
    print('\nYou pressed Ctrl+C!\n')
    outputHandling.close_player(channel_player)
    outputHandling.close_player(background_noise)
    mouse.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# execution

print("\n---------------------------------------------------------------------")
print(f" Starting loop with initial position {position} and maximum position {position_max_value}")
print("---------------------------------------------------------------------\n")
while True:

    position = calculate_position(velocity, position, position_max_value)

    new_closest_channel = find_closest_channel(position, channel_list)
    if new_closest_channel != closest_channel:
        closest_channel = new_closest_channel
        channel_player.set_new_channel_config(closest_channel)

    if last_second != datetime.datetime.now().second:
        print("position: " + str(position))
        last_second = datetime.datetime.now().second

    channel_volume = channel_player.set_volume_based_on_position(position)
    background_noise.set_volume(100 - channel_volume)

    velocity = mouse.read_movement() * config.SPEED_ADJUSTMENT_FACTOR