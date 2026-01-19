import arcade
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from scenes.menu_scene import MenuScene

class GameWindow(arcade.Window):
    def init(self):
        super().init(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color((20, 20, 30))

        self.current_scene = None
        self.show_menu()

    def show_menu(self):
        self.current_scene = MenuScene(self)

    def show_game(self):
        from scenes.game_scene import GameScene
        self.current_scene = GameScene(self)

    def on_draw(self):
        arcade.start_render()
        if self.current_scene:
            self.current_scene.on_draw()

    def on_update(self, delta_time):
        if self.current_scene:
            self.current_scene.on_update(delta_time)

    def on_key_press(self, key, modifiers):
        if self.current_scene:
            self.current_scene.on_key_press(key, modifiers)
