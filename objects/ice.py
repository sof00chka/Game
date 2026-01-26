import arcade


class Ice(arcade.Sprite):
    def __init__(self, x, y, scale=1):
        super().__init__(scale)

        self.center_x = x
        self.center_y = y

        # коэффициент скольжения
        self.friction = 0.98
