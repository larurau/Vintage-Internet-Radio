import time
import os

# sets initial station number to channel 8
station = 1

os.system("mpc play " + str(station))

# while True:
    # slight pause to debounce
    # time.sleep(0.05)