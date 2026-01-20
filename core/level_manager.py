from objects.wall import Wall
from objects.coin import Coin
from objects.enemy import Enemy


class LevelManager:
    def __init__(self):
        self.current_level = 1

    def load_level(self, level_number):
        walls = []
        coins = []
        spawn_point = (200, 200)

        if level_number == 1:
            spawn_point = (200, 200)
            walls = [
                Wall(400, 300, 200, 40),
                Wall(700, 500, 40, 200),
            ]
            coins = [
                Coin(900, 300)
            ]
            enemies = [ Enemy(800, 250)]

        elif level_number == 2:
            spawn_point = (150, 150)  # ← безопасная зона
            walls = [
                Wall(300, 600, 300, 40),
                Wall(600, 400, 40, 300),
            ]
            coins = [
                Coin(900, 700)
            ]
            enemies = [Enemy(800, 250)]

        elif level_number == 3:
            spawn_point = (150, 150)  # безопасный старт в углу

            walls = [
                Wall(400, 200, 300, 40),
                Wall(400, 500, 300, 40),

                Wall(700, 350, 40, 300),

                Wall(1000, 200, 300, 40),
                Wall(1000, 500, 300, 40),
            ]

            coins = [
                Coin(1200, 350)
            ]
            enemies = [Enemy(800, 250)]

        return walls, coins, enemies, spawn_point
