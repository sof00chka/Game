import arcade
from scenes.base_scene import BaseScene


class LoseScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)

        self.text = arcade.Text(
            "ПОРАЖЕНИЕ\n\n"
            "Все жизни потеряны.\n\n"
            "[ ENTER ]  В меню\n"
            "[ ESC ]    Выход",
            window.width // 2,
            window.height // 2,
            arcade.color.RED,
            font_size=22,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=500,
            align="center"
        )

    def on_draw(self):
        self.clear()
        self.text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_menu()
        elif key == arcade.key.ESCAPE:
            arcade.exit()
