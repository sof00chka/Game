import arcade
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, ICE_SPEED


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

        self.slide_texture = arcade.load_texture("resources/penguin/penguin_slide.png")

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1
        self.is_walking = False
        self.facing_right = True

        self.is_sliding = False
        self.slide_direction = None
        self.original_speed = (0, 0)
        self.target_x = None
        self.ice_section = None
        self.ice_side = None

        self.texture = self.walk_textures[0]

    def update_animation(self, delta_time):
        if self.is_sliding:
            self.texture = self.slide_texture
            return

        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture = (self.current_texture + 1) % len(self.walk_textures)
                self.texture = self.walk_textures[self.current_texture]

                if self.change_x < 0:
                    self.scale_x = -1.5
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

    def start_sliding(self, ice_sprite, ice_sections, ice_list):
        if self.is_sliding:
            return

        self.is_sliding = True
        self.original_speed = (self.change_x, self.change_y)
        self.ice_section = self.find_ice_section(ice_sprite, ice_sections)

        self.ice_side = self.determine_ice_side(ice_sprite)
        slide_to_right = self.should_slide_right()
        self.calculate_slide_target(slide_to_right)
        self.setup_slide_visuals(slide_to_right)
        self.is_walking = False

    def determine_ice_side(self, ice_sprite):
        vertical_distance = self.center_y - ice_sprite.center_y

        total_height = (self.height / 2) + (ice_sprite.height / 2)

        if abs(vertical_distance) < total_height * 0.3:
            if self.change_y > 0:
                return "bottom"
            else:
                return "top"
        elif vertical_distance > 0:
            return "bottom"
        else:
            return "top"

    def should_slide_right(self):
        if abs(self.change_x) > 0:
            return self.change_x > 0

        return self.facing_right

    def calculate_slide_target(self, slide_to_right):
        if not self.ice_section:
            return

        x_coords = []
        for ice in self.ice_section:
            x_coords.append(ice.left)
            x_coords.append(ice.right)

        if slide_to_right:
            self.target_x = max(x_coords)
        else:
            self.target_x = min(x_coords)

        if slide_to_right:
            self.change_x = ICE_SPEED
        else:
            self.change_x = -ICE_SPEED

        self.change_y = 0

    def setup_slide_visuals(self, slide_to_right):
        if slide_to_right:
            self.scale_x = 1.5
        else:
            self.scale_x = -1.5

        self.scale_y = 1.5

    def update_sliding(self, delta_time, ice_list):
        if not self.is_sliding or self.target_x is None:
            return True

        if not self.check_if_touching_ice(ice_list):
            self.stop_sliding()
            return True

        current_ice = self.get_current_ice(ice_list)
        if current_ice:
            new_side = self.determine_ice_side(current_ice)
            if new_side != self.ice_side:
                self.ice_side = new_side

        self.center_x += self.change_x * delta_time

        if (self.change_x > 0 and self.center_x >= self.target_x) or \
                (self.change_x < 0 and self.center_x <= self.target_x):
            self.stop_sliding()
            return True

        return False

    def get_current_ice(self, ice_list):
        for ice_sprite in ice_list:
            if arcade.check_for_collision(self, ice_sprite):
                return ice_sprite
        return None

    def check_if_touching_ice(self, ice_list):
        for ice_sprite in ice_list:
            if arcade.check_for_collision(self, ice_sprite):
                return True
        return False

    def stop_sliding(self):
        self.is_sliding = False
        self.ice_section = None
        self.target_x = None
        self.ice_side = None

        orig_x, orig_y = self.original_speed
        self.change_x = orig_x
        self.change_y = orig_y

        if self.facing_right:
            self.scale_x = 1.5
        else:
            self.scale_x = -1.5
        self.scale_y = 1.5

        self.texture = self.walk_textures[0]

    def find_ice_section(self, ice_sprite, ice_sections):
        for section in ice_sections:
            if ice_sprite in section:
                return section
        return [ice_sprite]

    def update(self, delta_time):
        if self.is_sliding:
            pass
        else:
            self.center_x += self.change_x * delta_time
            self.center_y += self.change_y * delta_time
            self.is_walking = abs(self.change_x) > 0.1 or abs(self.change_y) > 0.1

        self.update_animation(delta_time)
