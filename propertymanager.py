import json


class PropertyManager:

    def __init__(self):
        f = open("./config/config.json", "r", encoding="utf-8")
        self.properties = json.load(f)
        f.close()

    def get_ffmpeg_path(self):
        return self.properties["ffmpegPath"]

    def get_channel_lookup_url(self):
        return self.properties["channelLookupUrl"]

    def get_channel_url(self):
        return self.properties["channelUrl"]

    def get_discovery_service_url(self):
        return self.properties["discoveryServiceUrl"]

    def get_library_path(self):
        return self.properties["libraryPath"]