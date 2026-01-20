import arcade
from core.level_manager import LevelManager
from scenes.base_scene import BaseScene
from objects.player import Player
from core.constants import (
    PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT,
    WORLD_WIDTH, WORLD_HEIGHT, CAMERA_LERP
)


class GameScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)
        self.text = arcade.Text(
            "GAME SCENE\nESC - Back to menu",
            400,
            300,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )
        self.all_sprites = arcade.SpriteList()

        self.player = Player()
        self.all_sprites.append(self.player)

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.world_camera.position = (self.player.center_x, self.player.center_y)

        self.level_manager = LevelManager()
        self.level_index = 1

        self.load_level(self.level_index)

        self.level_text = arcade.Text(
            "",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            16
        )

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.all_sprites.draw()
        self.gui_camera.use()
        self.level_text.text = f"Level: {self.level_index}"
        self.level_text.draw()
        self.text.draw()

    def on_update(self, delta_time: float):
        self.physics_engine.update()

        enemies_hit = arcade.check_for_collision_with_list(
            self.player,
            self.enemy_list
        )

        if enemies_hit:
            self.window.show_menu()
            return

        cam_x, cam_y = self.world_camera.position
        player_x, player_y = self.player.center_x, self.player.center_y

        coins_hit = arcade.check_for_collision_with_list(
            self.player,
            self.coin_list
        )

        if coins_hit:
            for coin in coins_hit:
                coin.remove_from_sprite_lists()

            self.level_index += 1
            if self.level_index > 3:
                self.level_index = 1
            self.load_level(self.level_index)

        smooth_x = cam_x + (player_x - cam_x) * CAMERA_LERP
        smooth_y = cam_y + (player_y - cam_y) * CAMERA_LERP

        half_w = SCREEN_WIDTH // 2
        half_h = SCREEN_HEIGHT // 2
        smooth_x = max(half_w, min(WORLD_WIDTH - half_w, smooth_x))
        smooth_y = max(half_h, min(WORLD_HEIGHT - half_h, smooth_y))

        self.world_camera.position = (smooth_x, smooth_y)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_menu()
        elif key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED
        elif key == arcade.key.N:
            self.level_index += 1
            if self.level_index > 3:
                self.level_index = 1
            self.load_level(self.level_index)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def load_level(self, level_number):
        self.wall_list.clear()
        self.coin_list.clear()
        self.enemy_list.clear()

        for sprite in self.all_sprites[:]:
            if sprite != self.player:
                sprite.remove_from_sprite_lists()

        walls, coins, enemies, spawn_point = self.level_manager.load_level(level_number)

        for wall in walls:
            self.wall_list.append(wall)
            self.all_sprites.append(wall)

        for coin in coins:
            self.coin_list.append(coin)
            self.all_sprites.append(coin)

        for enemy in enemies:
            self.enemy_list.append(enemy)
            self.all_sprites.append(enemy)

        self.player.center_x, self.player.center_y = spawn_point
        self.world_camera.position = spawn_point



