import datetime
import signal
import sys

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
    channel = None
    min_distance = float('inf')  # Start with a large number

    for channel in channels:
        distance = abs(current_position - channel.position)
        if distance < min_distance:
            min_distance = distance
            channel = channel

    return channel

# setup

mouse = MouseDevice(1133, 49256)

position = 1000
position_max_value = 11400
last_second = datetime.datetime.now().second
velocity = 0

channel_list = [
    ChannelConfig(500, 50, 400, "https://cast1.torontocast.com:2170/;.mp3"),
    ChannelConfig(2500, 40, 500, "http://usa9.fastcast4u.com/proxy/jamz?mp=/1"),
    ChannelConfig(4000, 30, 600, "https://cast1.torontocast.com:2060/;.mp3"),
    ChannelConfig(5000, 20, 100, "https://a5.asurahosting.com:7640/radio.mp3"),
    ChannelConfig(5500, 30, 300, "https://fluxfm.streamabc.net/flx-chillhop-mp3-128-8581707"),
    ChannelConfig(6100, 40, 500, "https://ice1.somafm.com/deepspaceone-128-mp3"),
    ChannelConfig(6900, 80, 200, "https://radio.vintageobscura.net/stream"),
    ChannelConfig(7500, 50, 400, "http://gyusyabu.ddo.jp:8000/;stream.mp3"),
    ChannelConfig(8100, 100, 200, "https://s3.radio.co/sc8d895604/listen"),
    ChannelConfig(8400, 20, 100, "https://radio.weatherusa.net/NWR/KIG86.mp3"),
    ChannelConfig(8900, 70, 400, "http://radio.streemlion.com:3710/stream"),
    ChannelConfig(9800, 50, 350, "https://ice6.somafm.com/vaporwaves-128-mp3"),
    ChannelConfig(10500, 30, 240, "https://mediaserv73.live-streams.nl:18058/stream"),
    ChannelConfig(10900, 20, 120, "https://stream-153.zeno.fm/9q3ez3k3fchvv?zt=eyJhbGciOiJIUzI1NiJ9.eyJzdHJlYW0iOiI5cTNlejNrM2ZjaHZ2IiwiaG9zdCI6InN0cmVhbS0xNTMuemVuby5mbSIsInJ0dGwiOjUsImp0aSI6InFYeTZZdEZQU2hDTVN3ampEbUtvM3ciLCJpYXQiOjE3MjcwMTY4MDksImV4cCI6MTcyNzAxNjg2OX0.aeG5_KZQwVg_ImMkX6s-5ly83pua1F-tMMcY0VuDmoM"),
]

closest_channel = find_closest_channel(position, channel_list)

channel_player = InternetRadioPlayer(
    closest_channel,
    6600)
background_noise = FilePlayer(
    'noise.mp3',
    6601)

# signal handling

def signal_handler(_sig, _frame):
    print('\nYou pressed Ctrl+C!\n')
    outputHandling.close_player(channel_player)
    outputHandling.close_player(background_noise)
    mouse.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# execution

print("\nStarting loop ...")
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

    velocity = mouse.read_movement() / 3