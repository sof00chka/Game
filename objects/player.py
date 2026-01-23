import arcade
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale_x = 1.5
        self.scale_y = 1.5
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.speed = PLAYER_SPEED
        self.change_x = 0
        self.change_y = 0
        self.lives = 3
        self.walk_textures = []

        for i in range(1, 5):
            texture = arcade.load_texture(f"resources/penguin/penguin_walk0{i}.png")
            self.walk_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1
        self.is_walking = False
        self.facing_right = True

        self.texture = self.walk_textures[0]

    def update_animation(self, delta_time):
        """Обновление анимации"""
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture = (self.current_texture + 1) % len(self.walk_textures)
                self.texture = self.walk_textures[self.current_texture]

                if self.change_x < 0:
                    self.scale_x = -1.5  # отзеркаливания
                    self.scale_y = 1.5
                    self.facing_right = False
                elif self.change_x > 0:
                    self.scale_x = 1.5
                    self.scale_y = 1.5
                    self.facing_right = True
        else:
            self.texture = self.walk_textures[0]
            if self.facing_right:
                self.scale_x = 1.5
            else:
                self.scale_x = -1.5
            self.scale_y = 1.5

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.is_walking = abs(self.change_x) > 0.1 or abs(self.change_y) > 0.1
        self.update_animation(delta_time)
