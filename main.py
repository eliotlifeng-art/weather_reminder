import os
import sys

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from app.database import Database
from app.scheduler import ReminderScheduler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KV_DIR = os.path.join(BASE_DIR, "ui", "kv")

for kv_file in ["home.kv", "forecast.kv", "settings.kv", "city_manage.kv"]:
    kv_path = os.path.join(KV_DIR, kv_file)
    if os.path.exists(kv_path):
        Builder.load_file(kv_path)


class WeatherReminderApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.scheduler = ReminderScheduler(self.db)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Orange"

        sm = ScreenManager()
        from ui.screens.home import HomeScreen
        from ui.screens.forecast import ForecastScreen
        from ui.screens.settings import SettingsScreen
        from ui.screens.city_manage import CityManageScreen

        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ForecastScreen(name="forecast"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(CityManageScreen(name="city_manage"))

        return sm

    def on_start(self):
        self.scheduler.start()

    def on_stop(self):
        self.scheduler.stop()

    def get_default_city(self):
        return self.db.get_default_city()

    def set_default_city(self, city_name):
        self.db.set_default_city(city_name)


if __name__ == "__main__":
    WeatherReminderApp().run()
