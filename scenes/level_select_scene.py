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

        self.error_text = arcade.Text(
            "",
            window.width // 2,
            100,
            arcade.color.RED,
            16,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=500,
            align="center"
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

        self.current_available_level = 1
        max_unlocked = 0
        for level in range(1, MAX_BIG_LEVEL + 1):
            if level in window.unlocked_big_levels:
                max_unlocked = level
        if max_unlocked < MAX_BIG_LEVEL:
            self.current_available_level = max_unlocked
        else:
            self.current_available_level = MAX_BIG_LEVEL

        self.buttons = []
        w = 300
        h = 80
        s = 20

        for i in range(MAX_BIG_LEVEL):
            level_num = i + 1
            left = window.width // 2 - w // 2
            bottom = ((window.height * 1.5) // MAX_BIG_LEVEL - h // MAX_BIG_LEVEL + (1 - i) *
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
        self.error_text.draw()

        for button in self.buttons:
            n = button["big_level"]

            if n == self.current_available_level + 1:
                color = arcade.color.GREEN
            elif n <= self.current_available_level:
                color = arcade.color.YELLOW
            else:
                color = arcade.color.GRAY

            arcade.draw_lbwh_rectangle_filled(
                button["left"],
                button["bottom"],
                button["width"],
                button["height"],
                color
            )

            arcade.Text(
                button["text"],
                button["left"] + button["width"] // 2,
                button["bottom"] + button["height"] // 2,
                arcade.color.BLACK,
                font_size=24,
                anchor_x="center",
                anchor_y="center"
            ).draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            if (btn["left"] <= x <= btn["left"] + btn["width"] and
                    btn["bottom"] <= y <= btn["bottom"] + btn["height"]):

                n = btn["big_level"]
                if n <= self.current_available_level + 1:
                    self.window.show_game(big_level=n)
                    return
                else:
                    self.error_text.text = (f"Уровень заблокирован!\nЧтобы разблокировать, пройдите уровень "
                                            f"{n - 1}")
                    return

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_game(big_level=1)

        elif key == arcade.key.ESCAPE:
            self.error_text.text = ""
            self.window.show_menu()
