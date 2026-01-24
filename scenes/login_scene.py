import arcade
from scenes.base_scene import BaseScene
from core.database import Database


class LoginScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)
        self.db = Database()
        self.mode = "login"

        self.title_text = arcade.Text(
            "CHRONO LABYRINTH",
            window.width // 2,
            window.height - 100,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center"
        )

        self.mode_text = arcade.Text(
            "ВХОД",
            window.width // 2,
            window.height - 180,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center"
        )

        self.username = ""
        self.password = ""
        self.active_field = "username"

        self.message = ""
        self.message_color = arcade.color.WHITE

        self.instructions = arcade.Text(
            "[TAB] - переключить поле\n"
            "[ENTER] - подтвердить\n"
            "[SHIFT] - переключить режим (Вход/Регистрация)\n"
            "[ESC] - выйти",
            window.width // 2,
            100,
            arcade.color.LIGHT_GRAY,
            font_size=16,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=400,
            align="center"
        )

    def on_draw(self):
        self.clear(arcade.color.BLACK)

        self.title_text.draw()
        self.mode_text.draw()
        self.instructions.draw()

        username_label = "Логин:"
        password_label = "Пароль:"

        username_color = arcade.color.YELLOW if self.active_field == "username" else arcade.color.WHITE
        arcade.Text(
            f"{username_label} {self.username}",
            self.window.width // 2,
            self.window.height // 2 + 40,
            username_color,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        ).draw()

        password_color = arcade.color.YELLOW if self.active_field == "password" else arcade.color.WHITE
        arcade.Text(
            f"{password_label} {'*' * len(self.password)}",
            self.window.width // 2,
            self.window.height // 2 - 20,
            password_color,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        ).draw()

        if self.message:
            arcade.Text(
                self.message,
                self.window.width // 2,
                self.window.height // 2 - 80,
                self.message_color,
                font_size=20,
                anchor_x="center",
                anchor_y="center"
            ).draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            if self.mode == "login":
                self.mode = "register"
                self.mode_text.text = "РЕГИСТРАЦИЯ"
                self.message = ""
            else:
                self.mode = "login"
                self.mode_text.text = "ВХОД"
                self.message = ""
            return

        if key == arcade.key.TAB:
            if self.active_field == "username":
                self.active_field = "password"
            else:
                self.active_field = "username"
            return

        if key == arcade.key.BACKSPACE:
            if self.active_field == "username" and self.username:
                self.username = self.username[:-1]
            elif self.active_field == "password" and self.password:
                self.password = self.password[:-1]
            return

        elif arcade.key.A <= key <= arcade.key.Z or arcade.key.KEY_0 <= key <= arcade.key.KEY_9:
            char = chr(key)
            if self.active_field == "username":
                self.username += char
            else:
                self.password += char
            return

        elif key == arcade.key.ENTER:
            if not self.username or not self.password:
                self.message = "Заполните все поля!"
                self.message_color = arcade.color.RED
                return

            if self.mode == "login":
                user = self.db.login_user(self.username, self.password)
                if user:
                    self.message = f"Добро пожаловать, {self.username}!"
                    self.message_color = arcade.color.GREEN
                    self.window.current_user = {
                        'username': self.username,
                        'level': user['level']
                    }
                    arcade.schedule(self.show_menu, 1.0)
                else:
                    self.message = "Неверный логин или пароль!"
                    self.message_color = arcade.color.RED

            elif self.mode == "register":
                success = self.db.register_user(self.username, self.password)
                if success:
                    self.message = f"Пользователь {self.username} зарегистрирован!"
                    self.message_color = arcade.color.GREEN
                    user = self.db.login_user(self.username, self.password)
                    if user:
                        self.window.current_user = {
                            'username': self.username,
                            'level': user['level']
                        }
                        arcade.schedule(self.show_menu, 1.0)
                else:
                    self.message = "Пользователь с таким именем уже существует!"
                    self.message_color = arcade.color.RED
            return

        elif key == arcade.key.ESCAPE:
            self.window.close()

    def show_menu(self, delta_time):
        arcade.unschedule(self.show_menu)
        self.window.show_menu()