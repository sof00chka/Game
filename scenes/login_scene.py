import arcade
import arcade.gui
from scenes.base_scene import BaseScene
from core.database import Database


class LoginScene(BaseScene):
    def __init__(self, window):
        super().__init__(window)
        self.db = Database()
        self.mode = "login"

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.main_box = arcade.gui.UIBoxLayout(vertical=True, space_between=25)

        title_label = arcade.gui.UILabel(
            text="CHRONO LABYRINTH",
            font_size=48,
            font_name="Arial",
            text_color=arcade.color.WHITE
        )
        self.main_box.add(title_label)

        self.mode_label = arcade.gui.UILabel(
            text="ВХОД В ИГРУ",
            font_size=32,
            text_color=arcade.color.YELLOW
        )
        self.main_box.add(self.mode_label)

        login_container = arcade.gui.UIBoxLayout(vertical=True, space_between=10)
        login_text_label = arcade.gui.UILabel(
            text="ЛОГИН:",
            font_size=24,
            text_color=arcade.color.WHITE
        )
        login_container.add(login_text_label)
        self.username_input = arcade.gui.UIInputText(
            text="",
            width=400,
            height=50,
            font_size=20
        )
        login_container.add(self.username_input)
        self.main_box.add(login_container)

        password_container = arcade.gui.UIBoxLayout(vertical=True, space_between=10)
        password_text_label = arcade.gui.UILabel(
            text="ПАРОЛЬ:",
            font_size=24,
            text_color=arcade.color.WHITE
        )
        password_container.add(password_text_label)
        self.password_input = arcade.gui.UIInputText(
            text="",
            width=400,
            height=50,
            font_size=20,
            password=True
        )
        password_container.add(self.password_input)
        self.main_box.add(password_container)

        buttons_box = arcade.gui.UIBoxLayout(vertical=False, space_between=30)
        self.login_button = arcade.gui.UIFlatButton(
            text="ВОЙТИ",
            width=180,
            height=60,
            font_size=24
        )
        self.login_button.on_click = self.on_login_click
        buttons_box.add(self.login_button)
        self.register_button = arcade.gui.UIFlatButton(
            text="РЕГИСТРАЦИЯ",
            width=180,
            height=60,
            font_size=24
        )
        self.register_button.on_click = self.on_register_click
        buttons_box.add(self.register_button)
        self.main_box.add(buttons_box)

        message_container = arcade.gui.UIAnchorLayout(width=500, height=60)
        self.message_label = arcade.gui.UILabel(
            text="",
            font_size=20,
            text_color=arcade.color.RED_DEVIL,
            width=500,
            align="center"
        )
        message_container.add(self.message_label, anchor_x="center", anchor_y="center")
        self.main_box.add(message_container)

        instructions_label = arcade.gui.UILabel(
            text="[TAB] - сменить режим (вход/регистрация)\n"
                 "[ENTER] - подтвердить\n"
                 "[ESC] - выход из игры",
            font_size=18,
            text_color=arcade.color.LIGHT_GRAY,
            width=500,
            multiline=True,
            align="center"
        )
        self.main_box.add(instructions_label)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(self.main_box)
        self.manager.add(anchor)

        self.current_input = self.username_input

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        self.manager.draw()

    def on_login_click(self, event):
        self.process_login()

    def on_register_click(self, event):
        self.process_register()

    def process_login(self):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.show_message("Заполните все поля!", arcade.color.RED)
            return

        user = self.db.login_user(username, password)
        if user:
            self.show_message(f"Добро пожаловать, {username}!", arcade.color.GREEN)
            self.window.current_user = {
                'username': username,
                'level': user['level']
            }
            arcade.schedule(self.show_menu, 1.0)
        else:
            self.show_message("Неверный логин или пароль!", arcade.color.RED)

    def process_register(self):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.show_message("Заполните все поля!", arcade.color.RED)
            return

        success = self.db.register_user(username, password)
        if success:
            self.show_message(f"Пользователь {username} зарегистрирован!",
                              arcade.color.GREEN)
            user = self.db.login_user(username, password)
            if user:
                self.window.current_user = {
                    'username': username,
                    'level': user['level']
                }
                arcade.schedule(self.show_menu, 1.0)
        else:
            self.show_message("Пользователь с таким именем уже существует!",
                              arcade.color.RED)

    def show_message(self, message, color):
        self.message_label.text = message
        self.message_label.text_color = color

    def show_menu(self, delta_time):
        arcade.unschedule(self.show_menu)
        self.window.show_menu()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.TAB:
            if self.mode == "login":
                self.mode = "register"
                self.mode_label.text = "РЕГИСТРАЦИЯ"
                self.mode_label.text_color = arcade.color.CYAN
            else:
                self.mode = "login"
                self.mode_label.text = "ВХОД"
                self.mode_label.text_color = arcade.color.YELLOW
            self.show_message("", arcade.color.WHITE)
            return

        elif key == arcade.key.ENTER:
            if self.mode == "login":
                self.process_login()
            else:
                self.process_register()
            return

        elif key == arcade.key.ESCAPE:
            self.window.close()

    def on_hide_view(self):
        self.manager.disable()
