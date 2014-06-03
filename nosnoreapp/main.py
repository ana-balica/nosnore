from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, NoTransition

from screens import SleepScreen, StatisticsScreen, SettingsScreen


class NosnoreApp(App):
    def build(self):
        self.manager = ScreenManager(transition=NoTransition())
        self.manager.add_widget(SleepScreen(name='sleep'))
        self.manager.add_widget(StatisticsScreen(name='statistics'))
        self.manager.add_widget(SettingsScreen(name='settings'))
        return self.manager


if __name__ == '__main__':
    Config.set('graphics', 'width', '320')
    Config.set('graphics', 'height', '480')
    NosnoreApp().run()