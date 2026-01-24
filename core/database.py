import sqlite3


class Database:
    def __init__(self):
        self.db_file = "game_database.db"
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                level INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def register_user(self, username, password):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, level) VALUES (?, ?, 0)",
                (username, password)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def login_user(self, username, password):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, level FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                'id': result[0],
                'level': result[1],
            }
        return None

    def update_user_progress(self, username, level):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT level FROM users WHERE username = ?",
            (username,)
        )
        current = cursor.fetchone()
        if current and level > current[0]:
            cursor.execute(
                "UPDATE users SET level = ? WHERE username = ?",
                (level, username)
            )
        conn.commit()
        conn.close()

    def get_top_players(self, limit=10):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, level FROM users ORDER BY level DESC LIMIT ?",
            (limit,)
        )
        players = cursor.fetchall()
        conn.close()
        return players