import arcade
import random
from scenes.base_scene import BaseScene
from objects.particle import Particle



class LoseScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)

        self.text = arcade.Text(
            "ПОРАЖЕНИЕ\n\n"
            "Все жизни потеряны.\n\n"
            "[ ENTER ]  В меню\n"
            "[ ESC ]    Выход",
            window.width // 2,
            window.height // 2,
            arcade.color.RED,
            font_size=22,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=500,
            align="center"
        )

        self.particles = arcade.SpriteList()
        self.dislike_texture = arcade.load_texture("resources/dislike.png")
        self.change_angle = random.uniform(-3, 3)

    def on_draw(self):
        self.clear()
        self.text.draw()
        self.particles.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_menu()
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def spawn_dislike(self):
        if len(self.particles) > 120:
            return

        particle = Particle(
            texture=self.dislike_texture,
            x=random.randint(0, self.window.width),
            y=self.window.height + 10,
            dx=random.uniform(-0.5, 0.5),
            dy=random.uniform(-4.0, -7.0),  # намного быстрее вниз
            gravity=0.25,  # сильнее ускорение
            lifetime=3.5,  # живут меньше
            scale=0.08,  # ещё мельче
            fade=True
        )

        self.particles.append(particle)

    def on_update(self, delta_time):
        if random.random() < 0.25:
            self.spawn_dislike()
        self.particles.update(delta_time)




