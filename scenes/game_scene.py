import arcade

from scenes.base_scene import BaseScene


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

    def on_draw(self):
        self.clear()
        self.text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_menu()
