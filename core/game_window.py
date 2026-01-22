import arcade

from scenes.game_scene import GameScene
from scenes.level_select_scene import LevelSelectScene
from scenes.menu_scene import MenuScene
from scenes.exit_scene import ExitScene
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from scenes.win_scene import WinScene
from scenes.lose_scene import LoseScene



class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.menu_music = arcade.Sound("resources/music/menu.mp3")
        self.menu_music_player = self.menu_music.play(loop=True, volume=0.5)

        self.current_scene = None
        self.show_menu()
        self.unlocked_big_levels = {1}

    def show_menu(self):
        if self.menu_music_player:
            self.menu_music_player.play()

        self.show_view(MenuScene(self))

    def show_game(self, big_level=1):
        if self.menu_music_player:
            self.menu_music_player.pause()

        self.current_scene = GameScene(self, big_level)
        self.show_view(self.current_scene)

    def show_exit(self):
        self.current_scene = ExitScene(self)
        self.show_view(self.current_scene)

    def on_update(self, delta_time: float):
        if self.current_scene:
            self.current_scene.on_update(delta_time)

    def show_win(self):
        self.show_view(WinScene(self))

    def show_lose(self):
        self.show_view(LoseScene(self))

    def unlock_big_level(self, level):
        self.unlocked_big_levels.add(level)

    def is_big_level_unlocked(self, level):
        return level in self.unlocked_big_levels

    def show_level_select(self):
        self.current_scene = LevelSelectScene(self)
        self.show_view(self.current_scene)





