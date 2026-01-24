import arcade
from scenes.base_scene import BaseScene
from core.database import Database


class LeaderboardScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)
        self.db = Database()

        self.title_text = arcade.Text(
            "РЕЙТИНГ ИГРОКОВ",
            window.width // 2,
            window.height - 100,
            arcade.color.WHITE,
            font_size=36,
            anchor_x="center"
        )

        self.players = self.db.get_top_players()

        self.back_text = arcade.Text(
            "[ESC] Назад",
            window.width // 2,
            50,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_draw(self):
        self.clear(arcade.color.BLACK)

        self.title_text.draw()
        self.back_text.draw()

        arcade.Text(
            "Место",
            self.window.width // 2 - 200,
            self.window.height - 150,
            arcade.color.YELLOW,
            font_size=20,
            anchor_x="center"
        ).draw()

        arcade.Text(
            "Игрок",
            self.window.width // 2,
            self.window.height - 150,
            arcade.color.YELLOW,
            font_size=20,
            anchor_x="center"
        ).draw()

        arcade.Text(
            "Уровней",
            self.window.width // 2 + 200,
            self.window.height - 150,
            arcade.color.YELLOW,
            font_size=20,
            anchor_x="center"
        ).draw()

        y_pos = self.window.height - 200
        for i, (username, level) in enumerate(self.players, 1):
            arcade.Text(
                str(i),
                self.window.width // 2 - 200,
                y_pos,
                arcade.color.WHITE,
                font_size=18,
                anchor_x="center"
            ).draw()

            user_color = arcade.color.GREEN if self.window.current_user and username == self.window.current_user[
                'username'] else arcade.color.WHITE
            arcade.Text(
                username,
                self.window.width // 2,
                y_pos,
                user_color,
                font_size=18,
                anchor_x="center"
            ).draw()

            arcade.Text(
                str(level),
                self.window.width // 2 + 200,
                y_pos,
                arcade.color.WHITE,
                font_size=18,
                anchor_x="center"
            ).draw()

            y_pos -= 40
            if y_pos < 100:
                break

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_menu()
