import arcade
import random


class Particle(arcade.Sprite):
    def __init__(
            self,
            texture,
            x,
            y,
            dx=0,
            dy=0,
            lifetime=1.0,
            scale=1.0,
            fade=True,
            gravity=0
    ):
        super().__init__(texture, scale)

        self.center_x = x
        self.center_y = y

        self.change_x = dx
        self.change_y = dy

        self.lifetime = lifetime
        self.timer = 0

        self.fade = fade
        self.gravity = gravity

    def update(self, delta_time):
        self.timer += delta_time

        self.change_y -= self.gravity * delta_time

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.fade:
            self.alpha = int(255 * (1 - self.timer / self.lifetime))

        if self.timer >= self.lifetime:
            self.remove_from_sprite_lists()
