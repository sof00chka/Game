import arcade

class Wall(arcade.Sprite):
    def __init__(self, x, y, width=50, height=50):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(width, arcade.color.GRAY, outer_alpha=200) #поменяем потом
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height