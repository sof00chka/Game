import arcade
import random
from objects.particle import Particle
from core.constants import MAX_BIG_LEVEL
from scenes.base_scene import BaseScene


class WinScene(BaseScene):
    def __init__(self, window, big_level):
        super().__init__(window)

        self.big_level = big_level
        self.particles = arcade.SpriteList()
        self.confetti_started = False

        if self.big_level == MAX_BIG_LEVEL:
            self.text = arcade.Text(
                "ПОБЕДА!\n\n"
                "Вы прошли все уровни 🎉\n\n"
                "[ ENTER ]  В меню\n"
                "[ ESC ]    Выход",
                window.width // 2,
                window.height // 2,
                arcade.color.LIGHT_GREEN,
                font_size=22,
                anchor_x="center",
                anchor_y="center",
                multiline=True,
                width=500,
                align="center"
            )
        else:
            self.text = arcade.Text(
                f"УРОВЕНЬ {self.big_level} ПРОЙДЕН!\n\n"
                f"Открыт уровень {self.big_level + 1}!\n\n"
                "[ ENTER ]  Следующий уровень\n"
                "[ M ]      В меню\n"
                "[ ESC ]    Выход",
                window.width // 2,
                window.height // 2,
                arcade.color.LIGHT_GREEN,
                font_size=22,
                anchor_x="center",
                anchor_y="center",
                multiline=True,
                width=500,
                align="center"
            )

    def on_draw(self):
        self.clear()
        self.draw_background()
        self.text.draw()
        self.particles.draw()

    def on_key_press(self, key, modifiers):
        if self.big_level == MAX_BIG_LEVEL:
            if key == arcade.key.ENTER:
                self.window.show_menu()
            elif key == arcade.key.ESCAPE:
                arcade.exit()
        else:
            if key == arcade.key.ENTER:
                self.window.show_game(self.big_level + 1)
            elif key == arcade.key.M:
                self.window.show_level_select()
            elif key == arcade.key.ESCAPE:
                arcade.exit()

    def spawn_confetti(self):
        colors = [
            arcade.color.RED,
            arcade.color.YELLOW,
            arcade.color.GREEN,
            arcade.color.BLUE,
            arcade.color.PURPLE,
            arcade.color.ORANGE
        ]

        for _ in range(6):
            texture = arcade.make_soft_square_texture(
                8,
                random.choice(colors),
                255
            )

            particle = Particle(
                texture=texture,
                x=random.randint(0, self.window.width),
                y=self.window.height + 10,
                dx=random.uniform(-1, 1),
                dy=random.uniform(-4, -2),  # ВНИЗ
                lifetime=3.0,
                scale=1.0,
                gravity=0
            )

            self.particles.append(particle)

    def on_update(self, delta_time):
        if not self.confetti_started:
            for _ in range(15):
                self.spawn_confetti()
            self.confetti_started = True

        self.particles.update(delta_time)
