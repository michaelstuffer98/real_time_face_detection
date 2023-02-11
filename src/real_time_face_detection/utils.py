import os
import json
from typing import Any


def image_dir_generator(path):
    for f in os.listdir(path):
        image_path = os.path.join(path, f)
        if os.path.isfile(image_path):
            yield image_path


def pad(box, padding, width, height):
    # apply padding
    (x, y, w, h) = box
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(width, x + w + padding) - x
    h = min(height, y + h + padding) - y
    return (x, y, w, h)


# Fancy output for progress, integer in range 0 to 1
def print_progress(progress: float):
    progress = int(progress * 10)
    print(" > ", progress * "##", (10 - progress) * "  ", "||", progress * 10.0, " %", end='\r')


class ConfigLoader:
    def __init__(self, filepath="src/real_time_face_detection/ressources/config.json"):
        self.filepath = filepath
        self.load_config(filepath)

    def load_config(self, filepath) -> dict:
        with open(filepath, 'r') as f:
            self.config = json.load(f)
        return self.config

    def get(self, key) -> Any:
        try:
            return self.config[key]
        except KeyError:
            return None

    def set(self, key, value) -> bool:
        try:
            with open(self.filepath, 'w') as f:
                self.config[key] = value
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            print('Error at saving config file, changes have not been saved')
            print(e)
            return False

    def __getitem__(self, key) -> Any:
        return self.get(key)
