from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp


class TimePickerField(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = dp(8)
        self.size_hint_y = None
        self.height = dp(48)

        self.hour_field = MDTextField(
            hint_text="HH",
            input_filter="int",
            max_text_length=2,
            size_hint_x=0.4,
        )
        self.separator = MDTextField(
            text=":",
            disabled=True,
            size_hint_x=0.1,
            halign="center",
        )
        self.minute_field = MDTextField(
            hint_text="MM",
            input_filter="int",
            max_text_length=2,
            size_hint_x=0.4,
        )

        self.add_widget(self.hour_field)
        self.add_widget(self.separator)
        self.add_widget(self.minute_field)

    def get_time(self):
        try:
            h = int(self.hour_field.text or "0")
            m = int(self.minute_field.text or "0")
            if 0 <= h <= 23 and 0 <= m <= 59:
                return h, m
        except ValueError:
            pass
        return None

    def set_time(self, hour, minute):
        self.hour_field.text = f"{hour:02d}"
        self.minute_field.text = f"{minute:02d}"
