from kivy.uix.screenmanager import Screen


class SleepScreen(Screen):
    def __init__(self, **kwargs):
        super(SleepScreen, self).__init__(**kwargs)
        self.ids.toggle_rec_btn.bind(on_press=self.toggle_btn) 

    def toggle_btn(self, *args):
        btn_label = self.ids.toggle_rec_btn.text
        if btn_label == "Start":
            self.ids.toggle_rec_btn.text = "Stop"
        else:
            self.ids.toggle_rec_btn.text = "Start"


class StatisticsScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass
