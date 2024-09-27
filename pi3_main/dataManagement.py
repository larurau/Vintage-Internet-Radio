class ChannelConfig:
    def __init__(self, perfect_range, perception_range, name, stream_url):
        self.position = None  # Will be set later dynamically
        self.perfect_range = perfect_range
        self.perception_range = perception_range
        self.name = name
        self.stream_url = stream_url