import arcade
from scenes.base_scene import BaseScene
from objects.player import Player
from objects.wall import Wall
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

        # # ТЕСТОВЫЕ СТЕНЫ
        # for (x, y) in [(300, 300), (200, 500), (600, 200)]:
        #     wall = Wall(x, y, 200, 50)
        #     self.wall_list.append(wall)
        #     self.all_sprites.append(wall)

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.world_camera.position = (self.player.center_x, self.player.center_y)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.all_sprites.draw()
        self.gui_camera.use()
        self.text.draw()

    def on_update(self, delta_time: float):
        x = self.player.center_x
        y = self.player.center_y
        self.player.update(delta_time)
        hit_list = arcade.check_for_collision_with_list(self.player, self.wall_list)
        if hit_list:
            self.player.center_x = x
            self.player.center_y = y
        cam_x, cam_y = self.world_camera.position
        player_x, player_y = self.player.center_x, self.player.center_y

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

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
