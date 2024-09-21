import datetime
import os

from mouseDevice import MouseDevice

# placeholder that simply starts playing

station = 1
os.system("mpc play " + str(station))

# methods

def calculate_position(change, previous_position, max_value):
    new_position = previous_position + change

    if new_position > max_value:
        new_position -= max_value
    elif new_position < 0:
        new_position = max_value + previous_position

    return new_position

# setup

mouse = MouseDevice(1133, 49256)

position = 1000
position_max_value = 2000
last_second = datetime.datetime.now().second

# execution

print("\nStarting loop ...")
while True:

    velocity = mouse.read_movement() / 3

    position = calculate_position(velocity, position, position_max_value)

    if last_second != datetime.datetime.now().second:
        print("position: " + str(position))
        last_second = datetime.datetime.now().second

    current_station = 1 if position > 1000 else 2

    if current_station != station:
        station = current_station
        os.system("mpc play " + str(station))