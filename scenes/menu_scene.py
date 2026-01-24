import arcade
from scenes.base_scene import BaseScene


class MenuScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)

        if window.current_user:
            user_text = f"Игрок: {window.current_user['username']} | Уровень: {window.current_user['level']}"
            self.user_text = arcade.Text(
                user_text,
                window.width // 2,
                window.height - 50,
                arcade.color.GREEN,
                font_size=18,
                anchor_x="center"
            )
        else:
            self.user_text = None

        self.title_text = arcade.Text(
            "CHRONO LABYRINTH",
            window.width // 2,
            window.height // 2 + 120,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center"
        )

        self.subtitle_text = arcade.Text(
            "Dynamic Maze. Shifting Time.",
            window.width // 2,
            window.height // 2 + 60,
            arcade.color.LIGHT_GRAY,
            font_size=18,
            anchor_x="center"
        )

        self.controls_text = arcade.Text(
            "[ ENTER ]  Начать игру\n"
            "[ L ]      Рейтинг игроков\n"
            "[ ESC ]    Выход",
            window.width // 2,
            window.height // 2 - 20,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=400,
            align="center"
        )

    def on_draw(self):
        self.clear()

        if self.user_text:
            self.user_text.draw()

        self.title_text.draw()
        self.subtitle_text.draw()
        self.controls_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_level_select()

        elif key == arcade.key.L:
            self.window.show_leaderboard()

        elif key == arcade.key.ESCAPE:
            self.window.show_exit()