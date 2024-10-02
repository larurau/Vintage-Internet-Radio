import concurrent
import datetime
import signal
import sys
import random
import time

import config
import outputHandling
from dataManagement import ChannelConfig
from inputHandling import MouseDevice
from ledHandling import LedManager
from outputHandling import StationPlayer, FilePlayer

# methods

def calculate_position(change, previous_position, max_value):

    new_position = previous_position + change

    if new_position > max_value:
        new_position -= max_value
    elif new_position < 0:
        new_position = max_value + previous_position

    return int(new_position)

def find_closest_channel(current_position, channels):
    calculated_channel = None
    min_distance = float('inf')  # Start with a large number

    for channel in channels:
        distance = abs(current_position - channel.position)
        if distance < min_distance:
            min_distance = distance
            calculated_channel = channel

    return calculated_channel

def calculate_channel_positions(channels):

    initial_position = 0
    current_position = initial_position

    local_random = random.Random(config.POSITION_CALCULATION_SEED)
    min_distance = config.INBETWEEN_DISTANCE_MIN
    max_distance = config.INBETWEEN_DISTANCE_MAX

    print(f"\nInitialise channel positions of {len(channels)} channels:")

    for index, channel in enumerate(channels):

        # space necessary "below"
        current_position += channel.perception_range

        channel.position = current_position
        print(f"Initialised \"{channel.name}\" at position {current_position}")

        # space necessary "above" as well as extra distance
        extra_distance = local_random.randint(min_distance, max_distance)
        print(f"Extra distance: {extra_distance}")
        current_position += channel.perception_range + extra_distance

    print("Finished calculating channel positions")
    print(f"Maximum position is {current_position}\n")
    return channels, current_position

def main():

    # setup
    start_time = time.time()

    channel_list = [ChannelConfig(**channel) for channel in config.CHANNEL_LIST]
    channel_list, position_max_value = calculate_channel_positions(channel_list)

    led_manager = LedManager()
    led_manager.startup()

    executor = concurrent.futures.ThreadPoolExecutor()
    for channel in channel_list:
        executor.submit(channel.preprocess)

    position = config.INITIAL_POSITION
    if config.INITIAL_POSITION_RANDOM:
        position = random.randint(0, position_max_value)
    last_second = datetime.datetime.now().second
    velocity = 0

    closest_channel = find_closest_channel(position, channel_list)

    mouse_future = executor.submit(MouseDevice, config.MOUSE_VENDOR_ID, config.MOUSE_PRODUCT_ID)
    channel_player_future = executor.submit(StationPlayer, closest_channel, config.MPD_PORT_1)
    background_noise_future = executor.submit(FilePlayer, 'noise.mp3', config.MPD_PORT_2)

    mouse = mouse_future.result()
    channel_player = channel_player_future.result()
    background_noise = background_noise_future.result()

    # signal handling
    def signal_handler(_sig, _frame):
        print('\nYou pressed Ctrl+C!\n')
        outputHandling.close_player(channel_player)
        outputHandling.close_player(background_noise)
        mouse.close()
        led_manager.stop()
        executor.shutdown(wait=False)
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    end_time = time.time()
    # execution

    print("\n---------------------------------------------------------------------")
    print(f" Startup took {(end_time - start_time):.4f} seconds")
    print(f" Starting loop with initial position {position} and maximum position {position_max_value}")
    print("---------------------------------------------------------------------\n")
    while True:

        if velocity is not None:

            velocity = velocity * config.SPEED_ADJUSTMENT_FACTOR

            position = calculate_position(velocity, position, position_max_value)

            new_closest_channel = find_closest_channel(position, channel_list)
            if new_closest_channel != closest_channel:
                closest_channel = new_closest_channel
                channel_player.set_new_channel_config(closest_channel)

            if last_second != datetime.datetime.now().second:
                last_second = datetime.datetime.now().second

            channel_volume = channel_player.set_volume_based_on_position(position)
            background_noise.set_volume(100 - channel_volume)
            led_manager.select_animation(channel_volume, new_closest_channel)

        velocity = mouse.read_movement()

if __name__ == "__main__":
    main()
