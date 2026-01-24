import arcade
from scenes.base_scene import BaseScene
from core.constants import MAX_BIG_LEVEL


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

        self.back_text = arcade.Text(
            "[ ENTER ] Продолжить игру\n"
                 "[ ESC ] Назад",
            window.width // 2,
            100,
            arcade.color.WHITE,
            22,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=500,
            align="center"
        )
        self.buttons = []
        w = 300
        h = 80
        s = 40

        for i in range(MAX_BIG_LEVEL):
            level_num = i + 1
            left = window.width // MAX_BIG_LEVEL - w // MAX_BIG_LEVEL
            bottom = (window.height // MAX_BIG_LEVEL - h // MAX_BIG_LEVEL + (1 - i) *
                      (h + s))

            button = {
                "big_level": level_num,
                "left": left,
                "bottom": bottom,
                "width": w,
                "height": h,
                "text": f"Большой уровень {level_num}"
            }
            self.buttons.append(button)

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        self.title.draw()
        self.back_text.draw()

        for button in self.buttons:
            arcade.draw_lbwh_rectangle_filled(
                button["left"],
                button["bottom"],
                button["width"],
                button["height"],
                arcade.color.GRAY
            )

            arcade.Text(
                button["text"],
                button["left"] + button["width"] // 2,
                button["bottom"] + button["height"] // 2,
                arcade.color.WHITE,
                font_size=24,
                anchor_x="center",
                anchor_y="center"
            ).draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            if (btn["left"] <= x <= btn["left"] + btn["width"] and
                    btn["bottom"] <= y <= btn["bottom"] + btn["height"]):
                self.window.show_game(big_level=btn["big_level"])
                return

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_game(big_level=1)

        elif key == arcade.key.ESCAPE:
            self.window.show_menu()
