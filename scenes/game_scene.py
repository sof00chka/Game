import arcade

from scenes.base_scene import BaseScene
from objects.player import Player
from core.constants import PLAYER_SPEED


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

    def on_draw(self):
        self.clear()
        self.text.draw()
        self.all_sprites.draw()

    def on_update(self, delta_time: float):
        self.player.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_menu()

        if key == arcade.key.UP:
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
