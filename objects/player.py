import arcade
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("resources/player.png")
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.speed = PLAYER_SPEED
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time: float):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.center_x = max(self.width / 2, min(SCREEN_WIDTH - self.width / 2, self.center_x))
        self.center_y = max(self.height / 2, min(SCREEN_HEIGHT - self.height / 2, self.center_y))