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
        send_command(self.pico, 'Color(227,87,11)')
        time.sleep(2)

    def select_animation(self, volume):
        if volume > 99 and self.isPerfect == False:
            print('Breathing')
            send_command(self.pico, 'Color(230,196,30)')
            send_command(self.pico, 'Animation=breathing')
            self.isPerfect = True
        elif volume < 96 and self.isPerfect:
            print('Noise')
            send_command(self.pico, 'Color(209,171,33)')
            send_command(self.pico, 'Animation=noise')
            self.isPerfect = False