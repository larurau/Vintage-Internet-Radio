import yt_dlp

class ChannelConfig:
    def __init__(self, perfect_range, perception_range, name, stream_url,
                 stream_type="radio", color=None, animation=None):

        self.position = None  # Will be set later dynamically
        self.perfect_range = perfect_range
        self.perception_range = perception_range
        self.name = name
        self.stream_url = stream_url
        self.color = color
        self.animation = animation
        self.stream_type = stream_type

    def __handle_youtube_url(self):

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestaudio',
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                self.stream_url,
                download=False
            )
            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result
            return video['url']

    def preprocess(self):
        if self.stream_type == "youtube":
            new_url = self.__handle_youtube_url()
            self.stream_url = new_url
            self.stream_type = 'radio'
