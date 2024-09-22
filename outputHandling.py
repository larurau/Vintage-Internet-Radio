import time
import mpd

def connect(player, address="localhost"):
    try:
        player.client.connect(address, player.port)
        print(f"Connected to MPD server at {address}:{player.port}")
    except mpd.ConnectionError as e:
        print(f"Failed to connect to MPD server: {e}")

def set_volume_of_player(player, volume):
    while True:
        try:
            # Use ping to check if the connection is alive
            player.client.ping()
            # Set the volume
            player.client.setvol(volume)
            break  # Exit loop if successful
        except mpd.ConnectionError:
            print("Connection lost while trying to set volume, retrying...")
            # Try reconnecting only if the client is not already connected
            try:
                connect(player)
            except mpd.ConnectionError as e:
                print(f"Failed to reconnect: {e}")
                time.sleep(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(1)

def close_player(player):
    player.client.close()
    player.client.disconnect()

class Channel:

    def __init__(self, position, perfect_range, perception_range, stream_url, port):
        self.position = position
        self.perfect_range = perfect_range
        self.perception_range = perception_range
        self.stream_url = stream_url
        self.port = port

        self.client = mpd.MPDClient()
        connect(self)
        self.play_stream()

    def set_volume_based_on_position(self, current_position):
        distance = abs(current_position - self.position)

        if distance <= self.perfect_range:
            new_volume = 100
        elif distance <= self.perception_range:
            new_volume = int(100 * (1 - (distance - self.perfect_range) / (self.perception_range - self.perfect_range)))
        else:
            new_volume = 0

        set_volume_of_player(self, new_volume)
        return new_volume

    def play_stream(self):
        try:
            self.client.clear()
            self.client.add(self.stream_url)
            self.client.play()
            print(f"Playing {self.stream_url}")
        except mpd.CommandError as e:
            print(f"MPD command error: {e}")

class FilePlayer:

    def __init__(self, file_path, port):
        self.file_path = file_path
        self.port = port

        self.client = mpd.MPDClient()
        connect(self)
        self.play_file()

    def set_volume(self, current_position):
        set_volume_of_player(self, current_position)

    def play_file(self):
        try:
            self.client.clear()
            self.client.add('noise.mp3')
            self.client.repeat(1)
            self.client.play()
            print(f"Now playing: {self.file_path} on loop")
        except mpd.CommandError as e:
            print(f"MPD command error: {e}")