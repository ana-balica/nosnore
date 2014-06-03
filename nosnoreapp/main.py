from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, NoTransition

from screens import SleepScreen, StatisticsScreen, SettingsScreen


BACK_KEY = 27


class NosnoreApp(App):
    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def build(self):
        self.manager = ScreenManager(transition=NoTransition())
        self.manager.add_widget(SleepScreen(name='sleep'))
        self.manager.add_widget(StatisticsScreen(name='statistics'))
        self.manager.add_widget(SettingsScreen(name='settings'))
        return self.manager

    def hook_keyboard(self, window, key, *args):
        if key == BACK_KEY:
            self.manager.current = 'sleep'
            return True


if __name__ == '__main__':
    Config.set('graphics', 'width', '320')
    Config.set('graphics', 'height', '480')
    NosnoreApp().run()