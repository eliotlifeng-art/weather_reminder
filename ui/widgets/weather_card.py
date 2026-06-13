from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp


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
