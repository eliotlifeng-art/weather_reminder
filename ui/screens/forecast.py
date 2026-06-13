from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.clock import Clock


class ForecastItem(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(64)
        self.padding = [dp(12), dp(8)]
        self.spacing = dp(12)
        self.elevation = 1
        self.radius = [dp(8)]

        self.time_label = MDLabel(
            text="",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_x=0.35,
        )
        self.temp_label = MDLabel(
            text="",
            theme_text_color="Custom",
            text_color=(0.2, 0.6, 1, 1),
            font_style="Body1",
            halign="center",
            size_hint_x=0.25,
        )
        self.desc_label = MDLabel(
            text="",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_x=0.4,
        )

        self.add_widget(self.time_label)
        self.add_widget(self.temp_label)
        self.add_widget(self.desc_label)

    def update_data(self, item):
        dt = item.get("dt_txt", "")
        if " " in dt:
            time_part = dt.split(" ")[1][:5]
        else:
            time_part = dt
        self.time_label.text = time_part
        self.temp_label.text = f"{item['temp']:.1f}C"
        pop = item.get("pop", 0)
        desc = item.get("description", "")
        self.desc_label.text = f"{desc} | Rain {pop*100:.0f}%"


class ForecastScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        layout = MDBoxLayout(orientation="vertical")

        toolbar = MDTopAppBar(
            title="Forecast",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
        )
        layout.add_widget(toolbar)

        scroll = MDScrollView()
        self.content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(16),
            adaptive_height=True,
        )

        self.title_label = MDLabel(
            text="3-Hour Forecast",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(40),
        )
        self.content.add_widget(self.title_label)

        self.forecast_list = MDBoxLayout(
            orientation="vertical",
            spacing=dp(6),
            adaptive_height=True,
        )
        self.content.add_widget(self.forecast_list)

        scroll.add_widget(self.content)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_once(lambda dt: self.load_forecast(), 0.3)

    def load_forecast(self):
        self.forecast_list.clear_widgets()
        app = MDApp.get_running_app()
        api_key = app.db.get_setting("api_key", "")
        if not api_key:
            self.title_label.text = "Please set API Key in Settings"
            return

        from app.api import WeatherAPI
        api = WeatherAPI(api_key)
        city = app.get_default_city()
        if not city:
            return

        self.title_label.text = f"Forecast for {city['name']}"

        forecast_data = api.get_forecast(city_name=city.get("name"), lat=city.get("lat"), lon=city.get("lon"))
        forecast_list = WeatherAPI.parse_forecast(forecast_data)

        for item in forecast_list:
            fi = ForecastItem()
            fi.update_data(item)
            self.forecast_list.add_widget(fi)

    def go_back(self):
        self.manager.current = "home"
