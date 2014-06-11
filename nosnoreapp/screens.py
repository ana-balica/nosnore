from kivy.uix.screenmanager import Screen


class SleepScreen(Screen):
    def __init__(self, **kwargs):
        super(SleepScreen, self).__init__(**kwargs)
        self.ids.toggle_rec_btn.bind(on_press=self.toggle_btn) 

    def toggle_btn(self, *args):
        btn_label = self.ids.toggle_rec_btn.text
        sleep_label = self.ids.sleep_label.text
        if btn_label == "Start":
            self.ids.toggle_rec_btn.text = "Stop"
            self.ids.sleep_label.text = "Press the Stop button\nto end recording"
        else:
            self.ids.toggle_rec_btn.text = "Start"
            self.ids.sleep_label.text = "Time of recording - 8h\nTime of snoring - 2h\nChance of apnea - 24%"


class StatisticsScreen(Screen):
    pass


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.ids.settings_switch.bind(active=self.toggle_settings)

    def toggle_settings(self, *args):
        switch_active = self.ids.settings_switch.active
        checkboxes = self.ids.checkboxes
        if switch_active:
            for box in checkboxes.children:
                box.disabled = False
            self.ids.start_hour.disabled = False
            self.ids.start_minute.disabled = False
            self.ids.finish_hour.disabled = False
            self.ids.finish_minute.disabled = False
        else:
            for box in checkboxes.children:
                box.disabled = True
            self.ids.start_hour.disabled = True
            self.ids.start_minute.disabled = True
            self.ids.finish_hour.disabled = True
            self.ids.finish_minute.disabled = True
