import arcade
import math


class RotatingWallSection:
    def __init__(self, tiles):
        self.tiles = tiles
        if tiles:
            self.center_x = sum(t.center_x for t in tiles) / len(tiles)
            self.center_y = sum(t.center_y for t in tiles) / len(tiles)
            self.original_offsets = []
            for tile in tiles:
                self.original_offsets.append({
                    'tile': tile,
                    'dx': tile.center_x - self.center_x,
                    'dy': tile.center_y - self.center_y
                })

        for tile in self.tiles:
            tile.color = arcade.color.LIGHT_BLUE
            if hasattr(tile, 'alpha'):
                tile.alpha = 200

        self.should_rotate = False
        self.rotation_speed = 90
        self.is_rotating = False
        self.current_angle = 0

    def rotate_section(self):
        if not self.should_rotate or self.is_rotating or not self.tiles:
            return

        self.is_rotating = True

        self.current_angle = (self.current_angle + 90) % 360

        angle_rad = math.radians(self.current_angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        for offset in self.original_offsets:
            tile = offset['tile']
            dx = offset['dx']
            dy = offset['dy']

            new_dx = dx * cos_a - dy * sin_a
            new_dy = dx * sin_a + dy * cos_a

            tile.center_x = self.center_x + new_dx
            tile.center_y = self.center_y + new_dy

            tile.angle = self.current_angle

            tile.color = arcade.color.RED

        def reset_color(dt):
            for tile in self.tiles:
                tile.color = arcade.color.LIGHT_BLUE
            self.is_rotating = False

        arcade.schedule(reset_color, 0.3)

        self.should_rotate = False