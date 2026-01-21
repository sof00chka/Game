import arcade
from scenes.base_scene import BaseScene
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class PauseScene(BaseScene):
    def __init__(self, window, game_scene):
        super().__init__(window)
        self.game_scene = game_scene

        self.title_text = arcade.Text(
            "PAUSE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 80,
            arcade.color.WHITE,
            36,
            anchor_x="center"
        )

        self.resume_text = arcade.Text(
            "ENTER - Continue",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        self.menu_text = arcade.Text(
            "ESC - Main Menu",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 40,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

    def on_draw(self):
        # рисуем игру под паузой
        self.game_scene.on_draw()

        # затемнение
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )

        self.title_text.draw()
        self.resume_text.draw()
        self.menu_text.draw()
        if self.paused:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                (0, 0, 0, 180)
            )

            arcade.draw_text(
                "PAUSE",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 40,
                arcade.color.WHITE,
                32,
                anchor_x="center"
            )

            arcade.draw_text(
                "ESC - Continue",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 10,
                arcade.color.WHITE,
                16,
                anchor_x="center"
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_scene(self.game_scene)
        elif key == arcade.key.ESCAPE:
            self.window.show_menu()
