import arcade
import random


class Particle(arcade.Sprite):
    def __init__(self, texture, x, y, scale=1.0):
        super().__init__(texture, scale=scale)

        self.center_x = x
        self.center_y = y

        self.change_x = random.uniform(-2, 2)
        self.change_y = random.uniform(-6, -3)

        self.change_angle = random.uniform(-3, 3)

        self.lifetime = random.uniform(1.5, 3.0)
        self.fade_rate = 180

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.change_y -= 0.2  # гравитация

        self.angle += self.change_angle

        self.lifetime -= delta_time
        self.alpha -= self.fade_rate * delta_time

        if self.lifetime <= 0 or self.alpha <= 0:
            self.remove_from_sprite_lists()
