import arcade

from scenes.pause_scene import PauseScene
from scenes.base_scene import BaseScene
from objects.player import Player
from core.constants import (
    PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT,
    WORLD_WIDTH, WORLD_HEIGHT, CAMERA_LERP
)

from objects.dynamic_elements import RotatingWallSection
from core.maze_manager import MazeManager


class GameScene(BaseScene):
    def __init__(self, window, big_level=1):
        super().__init__(window)

        self.background = arcade.load_texture("resources/background.png")

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

        self.player_sprite = arcade.SpriteList()
        self.player = Player()
        self.player_sprite.append(self.player)

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()
        self.teleport_list = arcade.SpriteList()

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.score = 0

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

        self.rotation_timer_text = arcade.Text(
            "",
            SCREEN_WIDTH - 20,
            SCREEN_HEIGHT - 80,
            arcade.color.YELLOW,
            16,
            anchor_x="right"
        )

        self.maze_manager = MazeManager()

        self.big_level = big_level
        self.sub_level = 1
        self.max_sub_levels = {
            1: 3,
            2: 4
        }

        self.teleport_cooldown = 0
        self.teleport_pairs = {}
        self.last_teleport = None
        self.just_teleported = False

        # Загружаем музыку и звуки
        self.game_music = arcade.Sound("resources/music/game.mp3")
        self.menu_music = arcade.Sound("resources/music/menu.mp3")
        self.teleport_music = arcade.Sound("resources/music/teleport.mp3")
        self.wall_hit_music = arcade.Sound("resources/music/move_walls.mp3")
        self.lava_hit_music = arcade.Sound("resources/music/lava.mp3")
        self.coin_music = arcade.Sound("resources/music/coin.mp3")
        self.exit_music = arcade.Sound("resources/music/exit.mp3")
        self.game_over = arcade.Sound("resources/music/game_over.mp3")

        self.music_player = None

        self.load_level()

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_list
        )

    # ---------------- Рисование ----------------

    def on_draw(self):
        self.clear()

        self.world_camera.use()

        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            WORLD_WIDTH // 2, WORLD_HEIGHT // 2, WORLD_WIDTH, WORLD_HEIGHT))

        self.all_sprites.draw()

        self.player_sprite.draw()

        self.gui_camera.use()
        self.level_text.text = f"Level: {self.big_level}-{self.sub_level}"
        self.level_text.draw()

        self.ui_text.text = f"Score: {self.score}   Lives: {self.player.lives}"
        self.ui_text.draw()

    # ---------------- Обновление ----------------

    def on_update(self, delta_time: float):

        self.player.update(delta_time)

        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= delta_time

        if self.just_teleported:
            teleport_hit = arcade.check_for_collision_with_list(
                self.player, self.teleport_list
            )
            if not teleport_hit:
                self.just_teleported = False
                self.last_teleport = None

        if len(self.coin_list) > 0:
            self.physics_engine.update()
            for sprite in self.exit_list:
                if arcade.check_for_collision(self.player, sprite):
                    self.player.change_x = 0
                    self.player.change_y = 0
        else:
            self.physics_engine.update()

        self.maze_manager.update(delta_time)

        rotated_count = 0
        for section in self.maze_manager.rotating_sections:
            if section.should_rotate:
                section.rotate_section()
                rotated_count += 1

        if rotated_count > 0:
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player, self.wall_list
            )
            wall_hit = arcade.check_for_collision_with_list(
                self.player, self.wall_list
            )
            if wall_hit:
                self.wall_hit_music.play(volume=1.0)

                self.player.lives -= 1
                self.player.center_x = SCREEN_WIDTH // 2
                self.player.center_y = SCREEN_HEIGHT // 2

                if self.player.lives <= 0:
                    self.game_over.play()
                    self.window.show_lose()
                    return

        enemies_hit = arcade.check_for_collision_with_list(
            self.player, self.enemy_list
        )

        if enemies_hit:
            self.lava_hit_music.play(volume=1.0)

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
                self.coin_music.play()
                coin.remove_from_sprite_lists()
                self.score += 10

        if not self.just_teleported:
            teleport_hit = arcade.check_for_collision_with_list(
                self.player, self.teleport_list
            )

            if teleport_hit:
                self.handle_teleport(teleport_hit[0])

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
            self.exit_music.play()
            self.go_to_next_sub_level()
            return

    # ---------------- Телепорты ----------------

    def handle_teleport(self, teleport_sprite):
        if self.just_teleported:
            return

        if teleport_sprite == self.last_teleport:
            return

        teleport_id = self.get_teleport_id(teleport_sprite)

        if teleport_id in self.teleport_pairs:
            paired_teleports = self.teleport_pairs[teleport_id]

            for other_teleport in paired_teleports:
                if other_teleport != teleport_sprite:
                    self.teleport_music.play(volume=1.0)

                    self.last_teleport = other_teleport
                    self.just_teleported = True

                    self.player.center_x = other_teleport.center_x
                    self.player.center_y = other_teleport.center_y

                    self.teleport_cooldown = 0.3
                    cam_x, cam_y = self.world_camera.position
                    smooth_x = cam_x + (self.player.center_x - cam_x) * 0.5
                    smooth_y = cam_y + (self.player.center_y - cam_y) * 0.5

                    half_w = SCREEN_WIDTH // 2
                    half_h = SCREEN_HEIGHT // 2

                    smooth_x = max(half_w, min(WORLD_WIDTH - half_w, smooth_x))
                    smooth_y = max(half_h, min(WORLD_HEIGHT - half_h, smooth_y))

                    self.world_camera.position = (smooth_x, smooth_y)
                    break

    def get_teleport_id(self, teleport_sprite):
        if teleport_sprite.texture:
            return id(teleport_sprite.texture)
        return 0

    def setup_teleport_pairs(self):
        self.teleport_pairs.clear()

        for teleport in self.teleport_list:
            teleport_id = self.get_teleport_id(teleport)

            if teleport_id not in self.teleport_pairs:
                self.teleport_pairs[teleport_id] = []

            self.teleport_pairs[teleport_id].append(teleport)

    # ---------------- Кнопки ----------------

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pause_scene = PauseScene(self.window, self)
            self.window.show_view(pause_scene)
            return

        if key == arcade.key.R:
            self.maze_manager.rotate_random_sections()

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

    def load_level(self):
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list.clear()
        self.enemy_list.clear()
        self.exit_list.clear()
        self.teleport_list.clear()
        if hasattr(self, 'teleport_pairs'):
            self.teleport_pairs.clear()

        self.maze_manager.rotating_sections.clear()

        for sprite in self.all_sprites[:]:
            if sprite != self.player:
                sprite.remove_from_sprite_lists()

        map_path = f"resources/maps/big{self.big_level}_level{self.sub_level}.tmx"

        tile_map = arcade.load_tilemap(map_path, scaling=1.0)

        if "walls" in tile_map.sprite_lists:
            wall_sprites = tile_map.sprite_lists["walls"]
            for sprite in wall_sprites:
                if sprite.texture is not None:
                    self.wall_list.append(sprite)
                    self.all_sprites.append(sprite)

        if "rotating_walls" in tile_map.sprite_lists:
            rotating_sprites = tile_map.sprite_lists["rotating_walls"]
            rotating_tiles = [s for s in rotating_sprites if s.texture is not None]

            if rotating_tiles:
                sections = self.group_sect(rotating_tiles)

                for section_tiles in sections:
                    section = RotatingWallSection(section_tiles)

                    for tile in section_tiles:
                        self.remove_wall(tile.center_x, tile.center_y)

                        self.wall_list.append(tile)
                        self.all_sprites.append(tile)

                    self.maze_manager.add_rotating_section(section)

        if "coins" in tile_map.sprite_lists:
            self.coin_list = tile_map.sprite_lists["coins"]
            for coin in self.coin_list:
                self.all_sprites.append(coin)

        if "lava" in tile_map.sprite_lists:
            self.enemy_list.extend(tile_map.sprite_lists["lava"])
            for enemy in self.enemy_list:
                self.all_sprites.append(enemy)

        if "exit" in tile_map.sprite_lists:
            self.exit_list = tile_map.sprite_lists["exit"]
            for exit_sprite in self.exit_list:
                self.all_sprites.append(exit_sprite)

        if "teleports" in tile_map.sprite_lists:
            self.teleport_list = tile_map.sprite_lists["teleports"]
            for teleport in self.teleport_list:
                teleport.scale = 2.0
                self.all_sprites.append(teleport)

            self.setup_teleport_pairs()

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.last_teleport = None
        self.just_teleported = False
        self.teleport_cooldown = 0

        self.world_camera.position = (
            self.player.center_x, self.player.center_y
        )

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_list
        )

    # ---------------- Вспомогательные методы для вращающихся стен ----------------

    def group_sect(self, tiles):
        sections = []
        processed = set()

        for tile in tiles:
            if tile in processed:
                continue

            current_section = []
            to_process = [tile]

            while to_process:
                current = to_process.pop()
                if current in processed:
                    continue

                processed.add(current)
                current_section.append(current)

                for other in tiles:
                    if other in processed:
                        continue

                    dx = abs(current.center_x - other.center_x)
                    dy = abs(current.center_y - other.center_y)

                    if dx < 34 and dy < 34:
                        to_process.append(other)

            if current_section:
                sections.append(current_section)

        return sections

    def remove_wall(self, x, y):
        for wall in self.wall_list[:]:
            if (abs(wall.center_x - x) < 1 and
                    abs(wall.center_y - y) < 1):
                self.wall_list.remove(wall)
                if wall in self.all_sprites:
                    self.all_sprites.remove(wall)
                return True
        return False

    def on_show_view(self):
        if self.music_player is None:
            self.music_player = self.game_music.play(loop=True, volume=0.4)

    def on_hide_view(self):
        if self.music_player:
            self.music_player.pause()
            self.music_player = None

    def go_to_next_sub_level(self):
        if self.sub_level < 3:
            self.sub_level += 1
            self.load_level()
        else:
            self.window.show_win()

    def on_big_level_complete(self):
        self.window.unlock_big_level(self.big_level + 1)
        if self.music_player:
            self.music_player.pause()
            self.music_player = None
        self.window.show_menu()
