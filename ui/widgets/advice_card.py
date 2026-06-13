from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp


class AdviceCard(MDCard):
    def __init__(self, icon="information", text="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(56)
        self.padding = [dp(12), dp(8)]
        self.spacing = dp(12)
        self.elevation = 1
        self.radius = [dp(8)]

        self.add_widget(MDIconButton(icon=icon, disabled=True))
        self.add_widget(MDLabel(text=text, theme_text_color="Primary"))


class AdviceList(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(8)
        self.adaptive_height = True

    def update_advice(self, advice_list):
        self.clear_widgets()
        for a in advice_list:
            card = AdviceCard(icon=a["icon"], text=a["text"])
            self.add_widget(card)
