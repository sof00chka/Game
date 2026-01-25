import json

FILE = "stats.json"

class PlayerStats:
    def __init__(self):
        self.deaths = 0
        self.play_time = 0.0
        self.levels_completed = 0

    def save(self):
        with open(FILE, "w") as f:
            json.dump(self.__dict__, f, indent=4)
