import arcade

from scenes.base_scene import BaseScene


class GameScene(BaseScene):
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "GAME SCENE\nESC - Back to menu",
            400,
            300,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_menu()
