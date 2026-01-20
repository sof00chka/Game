import arcade

class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(
            "resources/cash.png",
            scale=2.0
        )
        self.center_x = x
        self.center_y = y
