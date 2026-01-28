import arcade
from scenes.base_scene import BaseScene


class ExitScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)

        self.text = arcade.Text(
            "Вы уверены, что хотите выйти?\n\n"
            "Несохранённый прогресс будет потерян.\n\n"
            "[ ESC ]  Выйти\n"
            "[ ENTER ]  Вернуться",
            window.width // 2,
            window.height // 2,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=500,
            align="center"
        )

    def on_draw(self):
        self.clear()
        self.draw_background()
        self.text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
        elif key == arcade.key.ENTER:
            self.window.show_menu()
