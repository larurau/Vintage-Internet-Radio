import time
import serial

def establish_connection():
    new_pico_connection = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    new_pico_connection.flush()
    return new_pico_connection

def send_command(pico_con ,command, wait_time=0, debug=False):
    pico_con.write(f"{command}\r".encode())
    if debug:
        print(f"Sent color command: {command}")
    time.sleep(wait_time)

    if pico_con.in_waiting > 0 & debug:
        resp = pico_con.readline().decode().strip()
        print(f"Received response: {resp}")
    time.sleep(wait_time)

if __name__ == "__main__":

    pico = establish_connection()

    while True:
        for color in ['red', 'green', 'blue']:
            send_command(pico, color, wait_time=1, debug=True)

class LedManager:

    def __init__(self):

        print("Initializing LedManager")
        self.pico = establish_connection()
        self.isPerfect = False

    def startup(self):
        send_command(self.pico, 'green')
        time.sleep(2)

    def select_animation(self, volume):
        if volume > 99 and self.isPerfect == False:
            send_command(self.pico, 'blue')
            self.isPerfect = True
        elif volume < 96 and self.isPerfect:
            send_command(self.pico, 'red')
            self.isPerfect = False