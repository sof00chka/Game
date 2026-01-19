import arcade

from scenes.base_scene import BaseScene
from objects.player import Player
from objects.wall import Wall

from core.constants import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT


class GameScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)
        self.text = arcade.Text(
            "GAME SCENE\nESC - Back to menu",
            400,
            300,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )
        self.all_sprites = arcade.SpriteList()
        self.player = Player()
        self.all_sprites.append(self.player)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # # ТЕСТОВЫЕ СТЕНЫ
        # for (x, y) in [(300, 300), (200, 500), (600, 200)]:
        #     wall = Wall(x, y, 200, 50)
        #     self.wall_list.append(wall)
        #     self.all_sprites.append(wall)

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()
        self.text.draw()

    def on_update(self, delta_time: float):
        x = self.player.center_x
        y = self.player.center_y
        self.player.update(delta_time)
        hit_list = arcade.check_for_collision_with_list(self.player, self.wall_list)
        if hit_list:
            self.player.center_x = x
            self.player.center_y = y

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_menu()

        elif key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
