import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "weather_reminder.db")


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                lat REAL,
                lon REAL,
                is_default INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hour INTEGER NOT NULL,
                minute INTEGER NOT NULL,
                enabled INTEGER DEFAULT 1,
                label TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
        """)
        if not self.get_cities():
            self.add_city("Beijing", is_default=True)
        if not self.get_reminders():
            self.add_reminder(7, 30, label="morning")
        conn.close()

    def get_cities(self):
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM cities ORDER BY is_default DESC, name").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add_city(self, name, lat=None, lon=None, is_default=False):
        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT INTO cities (name, lat, lon, is_default) VALUES (?, ?, ?, ?)",
                (name, lat, lon, 1 if is_default else 0),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()

    def remove_city(self, city_id):
        conn = self._get_conn()
        conn.execute("DELETE FROM cities WHERE id = ?", (city_id,))
        conn.commit()
        conn.close()

    def get_default_city(self):
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM cities WHERE is_default = 1 LIMIT 1").fetchone()
        if not row:
            row = conn.execute("SELECT * FROM cities LIMIT 1").fetchone()
        conn.close()
        return dict(row) if row else None

    def set_default_city(self, city_name):
        conn = self._get_conn()
        conn.execute("UPDATE cities SET is_default = 0")
        conn.execute("UPDATE cities SET is_default = 1 WHERE name = ?", (city_name,))
        conn.commit()
        conn.close()

    def get_reminders(self):
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM reminders ORDER BY hour, minute").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add_reminder(self, hour, minute, label=""):
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO reminders (hour, minute, enabled, label) VALUES (?, ?, 1, ?)",
            (hour, minute, label),
        )
        conn.commit()
        conn.close()

    def remove_reminder(self, reminder_id):
        conn = self._get_conn()
        conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        conn.commit()
        conn.close()

    def toggle_reminder(self, reminder_id, enabled):
        conn = self._get_conn()
        conn.execute("UPDATE reminders SET enabled = ? WHERE id = ?", (1 if enabled else 0, reminder_id))
        conn.commit()
        conn.close()

    def get_setting(self, key, default=None):
        conn = self._get_conn()
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        conn.close()
        return row["value"] if row else default

    def set_setting(self, key, value):
        conn = self._get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, str(value)),
        )
        conn.commit()
        conn.close()
