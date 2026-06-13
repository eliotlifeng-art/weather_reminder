from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.metrics import dp

from app.api import WeatherAPI
from app.advice import generate_advice, generate_notification_text
from app.notification import send_notification


class WeatherCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(200)
        self.padding = dp(16)
        self.spacing = dp(8)
        self.elevation = 3
        self.radius = [dp(12)]

        self.city_label = MDLabel(
            text="Loading...",
            theme_text_color="Primary",
            font_style="H5",
            halign="center",
        )
        self.temp_label = MDLabel(
            text="-- C",
            theme_text_color="Custom",
            text_color=(0.2, 0.6, 1, 1),
            font_style="H2",
            halign="center",
        )
        self.desc_label = MDLabel(
            text="",
            theme_text_color="Secondary",
            font_style="Body1",
            halign="center",
        )
        self.detail_label = MDLabel(
            text="",
            theme_text_color="Hint",
            font_style="Caption",
            halign="center",
        )

        self.add_widget(self.city_label)
        self.add_widget(self.temp_label)
        self.add_widget(self.desc_label)
        self.add_widget(self.detail_label)

    def update_data(self, current):
        if not current:
            self.city_label.text = "Failed to load"
            return
        self.city_label.text = current.get("city", "")
        self.temp_label.text = f"{current['temp']:.1f} C"
        self.desc_label.text = current.get("description", "").capitalize()
        self.detail_label.text = (
            f"Feels like {current['feels_like']:.1f}C | "
            f"Humidity {current['humidity']}% | "
            f"Wind {current['wind_speed']}m/s"
        )


class AdviceList(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(8)
        self.adaptive_height = True

    def update_advice(self, advice_list):
        self.clear_widgets()
        for a in advice_list:
            card = MDCard(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(56),
                padding=[dp(12), dp(8)],
                spacing=dp(12),
                elevation=1,
                radius=[dp(8)],
            )
            icon = MDIconButton(icon=a["icon"], disabled=True)
            label = MDLabel(text=a["text"], theme_text_color="Primary")
            card.add_widget(icon)
            card.add_widget(label)
            self.add_widget(card)


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = None
        self._dialog = None
        self._build_ui()

    def _build_ui(self):
        layout = MDBoxLayout(orientation="vertical")

        toolbar = MDTopAppBar(
            title="Weather Reminder",
            right_action_items=[
                ["refresh", lambda x: self.refresh_weather()],
                ["cog", lambda x: self.go_settings()],
                ["calendar-clock", lambda x: self.go_forecast()],
            ],
        )
        layout.add_widget(toolbar)

        scroll = MDScrollView()
        self.content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(16),
            adaptive_height=True,
        )

        self.weather_card = WeatherCard()
        self.content.add_widget(self.weather_card)

        btn_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8),
            padding=[0, dp(8)],
        )
        refresh_btn = MDRaisedButton(text="Refresh", on_release=lambda x: self.refresh_weather())
        notify_btn = MDRaisedButton(text="Test Notify", on_release=lambda x: self.test_notify())
        btn_layout.add_widget(refresh_btn)
        btn_layout.add_widget(notify_btn)
        self.content.add_widget(btn_layout)

        self.content.add_widget(MDLabel(
            text="Today's Advice",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(36),
        ))

        self.advice_list = AdviceList()
        self.content.add_widget(self.advice_list)

        scroll.add_widget(self.content)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_once(lambda dt: self.refresh_weather(), 0.5)

    def _get_api(self):
        app = MDApp.get_running_app()
        api_key = app.db.get_setting("api_key", "")
        if not api_key:
            self.weather_card.city_label.text = "Please set API Key in Settings"
            return None
        return WeatherAPI(api_key)

    def refresh_weather(self):
        api = self._get_api()
        if not api:
            return

        app = MDApp.get_running_app()
        city = app.get_default_city()
        if not city:
            return

        lat, lon = city.get("lat"), city.get("lon")
        city_name = city.get("name")

        current_data = api.get_current_weather(city_name=city_name, lat=lat, lon=lon)
        current = api.parse_current(current_data)
        self.weather_card.update_data(current)

        forecast_data = api.get_forecast(city_name=city_name, lat=lat, lon=lon)
        forecast_list = api.parse_forecast(forecast_data)

        advice = generate_advice(current, forecast_list)
        self.advice_list.update_advice(advice)

    def test_notify(self):
        api = self._get_api()
        if not api:
            return
        app = MDApp.get_running_app()
        city = app.get_default_city()
        if not city:
            return
        current_data = api.get_current_weather(city_name=city.get("name"))
        current = WeatherAPI.parse_current(current_data)
        text = generate_notification_text(current)
        send_notification("Weather Reminder", text)

    def go_settings(self):
        self.manager.current = "settings"

    def go_forecast(self):
        self.manager.current = "forecast"
