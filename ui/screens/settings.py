from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.metrics import dp


class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dialog = None
        self._time_dialog = None
        self._build_ui()

    def _build_ui(self):
        layout = MDBoxLayout(orientation="vertical")

        toolbar = MDTopAppBar(
            title="Settings",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
        )
        layout.add_widget(toolbar)

        scroll = MDScrollView()
        self.content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(16),
            adaptive_height=True,
        )

        self.content.add_widget(MDLabel(
            text="API Key",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(32),
        ))
        self.api_key_field = MDTextField(
            hint_text="Enter OpenWeatherMap API Key",
            size_hint_y=None,
            height=dp(48),
        )
        save_key_btn = MDRaisedButton(text="Save API Key", on_release=self.save_api_key)
        self.content.add_widget(self.api_key_field)
        self.content.add_widget(save_key_btn)

        self.content.add_widget(MDLabel(
            text="Cities",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(32),
            padding=[0, dp(16), 0, 0],
        ))
        add_city_btn = MDRaisedButton(
            text="Add City",
            on_release=self.show_add_city,
        )
        self.content.add_widget(add_city_btn)
        self.city_list = MDList()
        self.content.add_widget(self.city_list)

        self.content.add_widget(MDLabel(
            text="Reminder Times",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(32),
            padding=[0, dp(16), 0, 0],
        ))
        add_reminder_btn = MDRaisedButton(
            text="Add Reminder",
            on_release=self.show_add_reminder,
        )
        self.content.add_widget(add_reminder_btn)
        self.reminder_list = MDList()
        self.content.add_widget(self.reminder_list)

        scroll.add_widget(self.content)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def on_enter(self):
        self.load_settings()

    def load_settings(self):
        app = MDApp.get_running_app()

        api_key = app.db.get_setting("api_key", "")
        self.api_key_field.text = api_key if api_key else ""

        self.refresh_city_list()
        self.refresh_reminder_list()

    def save_api_key(self, *args):
        app = MDApp.get_running_app()
        key = self.api_key_field.text.strip()
        if key:
            app.db.set_setting("api_key", key)

    def refresh_city_list(self):
        self.city_list.clear_widgets()
        app = MDApp.get_running_app()
        cities = app.db.get_cities()
        for c in cities:
            is_default = c.get("is_default", 0)
            subtitle = "Default city" if is_default else "Tap to set as default"
            item = TwoLineAvatarIconListItem(
                text=c["name"],
                secondary_text=subtitle,
            )
            item.bind(on_release=lambda x, name=c["name"]: self.set_default_city(name))

            if not is_default:
                del_btn = IconRightWidget(icon="delete")
                del_btn.bind(on_release=lambda x, cid=c["id"]: self.delete_city(cid))
                item.add_widget(del_btn)

            self.city_list.add_widget(item)

    def set_default_city(self, name):
        app = MDApp.get_running_app()
        app.set_default_city(name)
        self.refresh_city_list()

    def delete_city(self, city_id):
        app = MDApp.get_running_app()
        app.db.remove_city(city_id)
        self.refresh_city_list()

    def show_add_city(self, *args):
        if not self._dialog:
            self._city_field = MDTextField(hint_text="City name (e.g. Shanghai)")
            self._dialog = MDDialog(
                title="Add City",
                type="custom",
                content_cls=self._city_field,
                buttons=[
                    MDFlatButton(text="Cancel", on_release=lambda x: self._dialog.dismiss()),
                    MDRaisedButton(text="Add", on_release=self._do_add_city),
                ],
            )
        self._city_field.text = ""
        self._dialog.open()

    def _do_add_city(self, *args):
        name = self._city_field.text.strip()
        if name:
            app = MDApp.get_running_app()
            app.db.add_city(name)
            self.refresh_city_list()
        self._dialog.dismiss()

    def refresh_reminder_list(self):
        self.reminder_list.clear_widgets()
        app = MDApp.get_running_app()
        reminders = app.db.get_reminders()
        for r in reminders:
            time_str = f"{r['hour']:02d}:{r['minute']:02d}"
            label = r.get("label", "") or "Reminder"
            item = TwoLineAvatarIconListItem(
                text=time_str,
                secondary_text=label,
            )
            del_btn = IconRightWidget(icon="delete")
            del_btn.bind(on_release=lambda x, rid=r["id"]: self.delete_reminder(rid))
            item.add_widget(del_btn)
            self.reminder_list.add_widget(item)

    def show_add_reminder(self, *args):
        if not self._time_dialog:
            self._hour_field = MDTextField(hint_text="Hour (0-23)", input_filter="int")
            self._minute_field = MDTextField(hint_text="Minute (0-59)", input_filter="int")
            box = MDBoxLayout(orientation="vertical", spacing=dp(8), adaptive_height=True)
            box.add_widget(self._hour_field)
            box.add_widget(self._minute_field)
            self._time_dialog = MDDialog(
                title="Add Reminder Time",
                type="custom",
                content_cls=box,
                buttons=[
                    MDFlatButton(text="Cancel", on_release=lambda x: self._time_dialog.dismiss()),
                    MDRaisedButton(text="Add", on_release=self._do_add_reminder),
                ],
            )
        self._hour_field.text = ""
        self._minute_field.text = ""
        self._time_dialog.open()

    def _do_add_reminder(self, *args):
        try:
            hour = int(self._hour_field.text)
            minute = int(self._minute_field.text)
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                app = MDApp.get_running_app()
                app.db.add_reminder(hour, minute)
                self.refresh_reminder_list()
        except ValueError:
            pass
        self._time_dialog.dismiss()

    def delete_reminder(self, reminder_id):
        app = MDApp.get_running_app()
        app.db.remove_reminder(reminder_id)
        self.refresh_reminder_list()

    def go_back(self):
        self.manager.current = "home"
