import arcade

from scenes.game_scene import GameScene
from scenes.menu_scene import MenuScene
from scenes.exit_scene import ExitScene
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.current_scene = None
        self.show_menu()

    def show_menu(self):
        self.current_scene = MenuScene(self)
        self.show_view(self.current_scene)

    def show_game(self):
        self.current_scene = GameScene(self)
        self.show_view(self.current_scene)

    def show_exit(self):
        self.current_scene = ExitScene(self)
        self.show_view(self.current_scene)

    def on_update(self, delta_time: float):
        if self.current_scene:
            self.current_scene.on_update(delta_time)
