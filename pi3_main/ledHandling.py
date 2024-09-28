import time
import serial

def establish_connection():
    new_pico_connection = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    new_pico_connection.flush()
    return new_pico_connection

def close_connection(connection):
    if connection.is_open:
        connection.close()

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
        self.animationState = ""

    def startup(self):
        send_command(self.pico, 'Color(227,87,11)')
        time.sleep(2)

    def stop(self):
        close_connection(self.pico)

    def select_animation(self, volume, channel):
        if 97 < volume  and self.animationState != "Breathing":

            if channel.color is None:
                send_command(self.pico, 'Color(230,196,30)')
            else:
                send_command(self.pico, f'Color{channel.color}')

            if channel.animation is None:
                send_command(self.pico, 'Animation(breathing)')
            else:
                send_command(self.pico, f'Animation({channel.animation})')

            self.animationState = "Breathing"

        elif 90 < volume < 97 and self.animationState != "LowNoise":

            send_command(self.pico, 'Color(209,171,33)')
            send_command(self.pico, 'Animation(noise)')
            send_command(self.pico, 'NoiseIntensity(0)')
            self.animationState = "LowNoise"

        elif 80 < volume < 90 and self.animationState != "MediumNoise":

            send_command(self.pico, 'Color(209,171,33)')
            send_command(self.pico, 'Animation(noise)')
            send_command(self.pico, 'NoiseIntensity(15)')
            self.animationState = "MediumNoise"

        elif 55 < volume < 80 and self.animationState != "Noise":

            send_command(self.pico, 'Color(209,171,33)')
            send_command(self.pico, 'Animation(noise)')
            send_command(self.pico, 'NoiseIntensity(50)')
            self.animationState = "Noise"

        elif 40 < volume < 55 and self.animationState != "MediumStrongNoise":

            send_command(self.pico, 'Color(209,171,33)')
            send_command(self.pico, 'Animation(noise)')
            send_command(self.pico, 'NoiseIntensity(100)')
            self.animationState = "MediumStrongNoise"

        elif 25 < volume < 40 and self.animationState != "StrongNoise":

            send_command(self.pico, 'Color(209,171,33)')
            send_command(self.pico, 'Animation(noise)')
            send_command(self.pico, 'NoiseIntensity(250)')
            self.animationState = "StrongNoise"

        elif volume < 25 and self.animationState != "VeryStrongNoise":

            send_command(self.pico, 'Color(209,171,33)')
            send_command(self.pico, 'Animation(noise)')
            send_command(self.pico, 'NoiseIntensity(600)')
            self.animationState = "VeryStrongNoise"