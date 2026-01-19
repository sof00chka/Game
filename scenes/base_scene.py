class BaseScene:
    def init(self, window):
        self.window = window

    def on_draw(self):
        pass

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, modifiers):
        pass