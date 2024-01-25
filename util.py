import os
from pathlib import Path

class Util:

    def __init__(self):
        pass

    @staticmethod
    def display_preceding_zeros(num : int):
        num_str = str(num)
        if (num < 10):
            return "00" + num_str
        if (num < 100):
            return "0" + num_str
        return num_str

    @staticmethod
    def get_latest_counter_for_stream_file(directory : str, username: str):
        latestClipNumber = 0
        wildcard = username + "*"
        directory = directory.replace("/", "\\")
        print("OUT>> "+ directory)
        for path in Path(directory).glob(wildcard):
            if (path.is_file()):
                latestClipNumber = int((str(path).split(username + "_")[1].replace(".mkv", "")))
        return Util.display_preceding_zeros(latestClipNumber + 1)

    @staticmethod
    def create(library_dir : str):
        dir = os.path.join(library_dir)
        if not os.path.exists(dir):
            os.makedirs(dir)

