import random
from core.constants import MOVE_INTERVAL


class MazeManager:
    def __init__(self):
        self.rotating_sections = []
        self.change_timer = 0
        # self.change_interval = 10.0
        self.last_rotation_time = 0

    def add_rotating_section(self, section):
        if section not in self.rotating_sections:
            self.rotating_sections.append(section)

    def update(self, delta_time: float):
        self.change_timer += delta_time
        self.last_rotation_time += delta_time

        if self.change_timer >= MOVE_INTERVAL and self.last_rotation_time >= 2.0:
            self.rotate_random_sections()
            self.change_timer = 0
            self.last_rotation_time = 0

    def rotate_random_sections(self):
        if not self.rotating_sections:
            return

        rotate_count = max(1, int(len(self.rotating_sections) * 0.3))

        sections_to_rotate = random.sample(
            self.rotating_sections,
            min(rotate_count, len(self.rotating_sections))
        )

        for section in sections_to_rotate:
            section.should_rotate = True

    def get_remaining_time(self):
        return max(0, MOVE_INTERVAL - self.change_timer)
