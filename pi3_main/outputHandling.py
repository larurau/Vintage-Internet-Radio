import time
import mpd
import yt_dlp

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

def handle_youtube_url(url):

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio',
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(
            url,
            download=False
        )
        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result
        return video['url']

class StationPlayer:

    def __init__(self, current_channel_config, port):
        self.current_channel_config = current_channel_config
        self.port = port

        self.client = mpd.MPDClient()
        connect(self)
        self.play_channel()

    def set_new_channel_config(self, new_channel_config):
        self.current_channel_config = new_channel_config
        self.play_channel()

    def set_volume_based_on_position(self, current_position):
        distance = abs(current_position - self.current_channel_config.position)

        if distance <= self.current_channel_config.perfect_range:
            new_volume = 100
        elif distance <= self.current_channel_config.perception_range:

            dividend = distance - self.current_channel_config.perfect_range
            divisor = self.current_channel_config.perception_range - self.current_channel_config.perfect_range

            relative_distance = dividend / divisor
            new_volume = int(100 * (1 - relative_distance))

        else:
            new_volume = 0

        set_volume_of_player(self, new_volume)
        return new_volume

    def play_channel(self):
        try:
            self.client.clear()

            if self.current_channel_config.stream_type == 'radio':
                self.client.add(self.current_channel_config.stream_url)
            if self.current_channel_config.stream_type == 'youtube':
                new_url = handle_youtube_url(self.current_channel_config.stream_url)
                self.current_channel_config.stream_url = new_url
                self.current_channel_config.stream_type = 'radio'
                self.client.add(new_url)

            self.client.play()
            print(f"Playing station \"{self.current_channel_config.name}\"")
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
            print(f"Playing file \"{self.file_path}\" on loop")
        except mpd.CommandError as e:
            print(f"MPD command error: {e}")
