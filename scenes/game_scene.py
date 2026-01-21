import arcade
import os

from scenes.base_scene import BaseScene
from objects.player import Player
from core.constants import (
    PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT,
    WORLD_WIDTH, WORLD_HEIGHT, CAMERA_LERP,
    MAX_LEVEL
)


class GameScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)

        self.text = arcade.Text(
            "GAME SCENE\nESC - Pause",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            font_size=70,
            anchor_x="center",
            anchor_y="center"
        )

        self.all_sprites = arcade.SpriteList()

        self.player = Player()
        self.all_sprites.append(self.player)

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.level_index = 1
        self.score = 0
        self.paused = False

        self.level_text = arcade.Text(
            "",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            16
        )

        self.ui_text = arcade.Text(
            "",
            20,
            SCREEN_HEIGHT - 60,
            arcade.color.WHITE,
            16
        )

        self.load_level(self.level_index)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_list
        )

    # ---------------- Рисование ----------------

    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.all_sprites.draw()

        self.gui_camera.use()
        self.level_text.text = f"Level: {self.level_index}"
        self.level_text.draw()

        self.ui_text.text = f"Score: {self.score}   Lives: {self.player.lives}"
        self.ui_text.draw()

        if self.paused:
            self.text.draw()

    # ---------------- Обновление ----------------

    def on_update(self, delta_time: float):
        if self.paused:
            return

        if len(self.coin_list) > 0:
            self.physics_engine.update()
            for sprite in self.exit_list:
                if arcade.check_for_collision(self.player, sprite):
                    self.player.change_x = 0
                    self.player.change_y = 0
        else:
            self.physics_engine.update()

        # --- столкновение с врагами ---
        enemies_hit = arcade.check_for_collision_with_list(
            self.player, self.enemy_list
        )

        if enemies_hit:
            self.player.lives -= 1
            self.player.center_x = SCREEN_WIDTH // 2
            self.player.center_y = SCREEN_HEIGHT // 2

            if self.player.lives <= 0:
                self.window.show_lose()
                return

        # --- сбор монет ---
        coin_hit = arcade.check_for_collision_with_list(
            self.player, self.coin_list
        )

        if coin_hit:
            for coin in coin_hit:
                coin.remove_from_sprite_lists()
                self.score += 10

        # --- камера ---
        cam_x, cam_y = self.world_camera.position
        px, py = self.player.center_x, self.player.center_y

        smooth_x = cam_x + (px - cam_x) * CAMERA_LERP
        smooth_y = cam_y + (py - cam_y) * CAMERA_LERP

        half_w = SCREEN_WIDTH // 2
        half_h = SCREEN_HEIGHT // 2

        smooth_x = max(half_w, min(WORLD_WIDTH - half_w, smooth_x))
        smooth_y = max(half_h, min(WORLD_HEIGHT - half_h, smooth_y))

        self.world_camera.position = (smooth_x, smooth_y)

        # --- портал (ТОЛЬКО если монет нет) ---
        exit_hit = arcade.check_for_collision_with_list(
            self.player, self.exit_list
        )

        if exit_hit and len(self.coin_list) == 0:

            # если последний уровень — победа
            if self.level_index == MAX_LEVEL:
                self.window.show_win()
                return

            # иначе следующий уровень
            self.level_index += 1
            self.load_level(self.level_index)
            return

    # ---------------- Кнопки ----------------

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            return

        if self.paused:
            return

        if key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0

    # ---------------- Загрузка уровней ----------------

    def load_level(self, level_number):
        self.wall_list.clear()
        self.coin_list.clear()
        self.enemy_list.clear()
        self.exit_list.clear()

        for sprite in self.all_sprites[:]:
            if sprite != self.player:
                sprite.remove_from_sprite_lists()

        map_name = f"level{level_number}.tmx"
        map_path = os.path.join("resources", map_name)

        tile_map = arcade.load_tilemap(map_path, scaling=1.0)

        if "walls" in tile_map.sprite_lists:
            self.wall_list = tile_map.sprite_lists["walls"]

        if "coins" in tile_map.sprite_lists:
            self.coin_list = tile_map.sprite_lists["coins"]

        if "lava" in tile_map.sprite_lists:
            self.enemy_list.extend(tile_map.sprite_lists["lava"])

        if "exit" in tile_map.sprite_lists:
            self.exit_list = tile_map.sprite_lists["exit"]

        for lst in (self.wall_list, self.coin_list, self.enemy_list, self.exit_list):
            for sprite in lst:
                self.all_sprites.append(sprite)

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.world_camera.position = (
            self.player.center_x, self.player.center_y
        )

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_list
        )