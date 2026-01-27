import arcade
import os

class BaseScene(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.background_list = None  # Список спрайтов для фона

        # Преобразуем имя класса в snake_case
        name = self.__class__.__name__
        scene_name = ''.join(
            '_' + c.lower() if c.isupper() else c
            for c in name
        ).lstrip('_')

        bg_path = f"resources/backgrounds/{scene_name}_background.jpg"

        if os.path.exists(bg_path):
            self.background_list = arcade.SpriteList()
            background_sprite = arcade.Sprite(bg_path)
            background_sprite.center_x = window.width / 2
            background_sprite.center_y = window.height / 2
            background_sprite.width = window.width
            background_sprite.height = window.height
            self.background_list.append(background_sprite)

    def draw_background(self):
        if self.background_list:
            self.background_list.draw()  # draw через SpriteList

    def on_draw(self):
        self.clear()
