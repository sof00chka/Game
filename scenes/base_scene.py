import arcade


class BaseScene(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time: float):
        pass
