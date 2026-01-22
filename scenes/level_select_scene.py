import arcade
from scenes.base_scene import BaseScene


class LevelSelectScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)

        self.title = arcade.Text(
            "ВЫБОР УРОВНЯ",
            window.width // 2,
            window.height - 100,
            arcade.color.WHITE,
            36,
            anchor_x="center"
        )

        self.levels_text = arcade.Text(
            "[ 1 ]  Большой уровень 1\n"
            "[ 2 ]  Большой уровень 2\n\n"
            "[ ESC ] Назад",
            window.width // 2,
            window.height // 2,
            arcade.color.WHITE,
            22,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=500,
            align="center"
        )

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        self.title.draw()
        self.levels_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.KEY_1:
            self.window.show_game(big_level=1)

        elif key == arcade.key.KEY_2:
            self.window.show_game(big_level=2)

        elif key == arcade.key.ESCAPE:
            self.window.show_menu()
