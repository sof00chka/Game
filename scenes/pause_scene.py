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
            "[ ENTER ]  Continue",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        self.menu_text = arcade.Text(
            "[ ESC ]  Main Menu",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 40,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        if self.game_scene.music_player:
            self.game_scene.music_player.pause()

        self.game_scene.music_player = self.game_scene.game_music.play(
            loop=True, volume=0.4
        )

    def on_draw(self):
        # Рисуем замороженную игру
        self.game_scene.on_draw()

        # Затемнение
        arcade.draw.draw_rect_filled(
            arcade.rect.XYWH(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            ),
            arcade.color.BLACK
        )

        self.title_text.draw()
        self.resume_text.draw()
        self.menu_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            # Возвращаемся в игру
            self.window.show_view(self.game_scene)

        elif key == arcade.key.ESCAPE:
            # В главное меню
            self.window.show_level_select()


