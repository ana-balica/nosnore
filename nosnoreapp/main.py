from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition


class MainScreen(Screen):
    pass


class NosnoreApp(App):
    def build(self):
        self.manager = ScreenManager(transition=NoTransition())
        self.manager.add_widget(MainScreen(name='menu'))
        return self.manager


if __name__ == '__main__':
    Config.set('graphics', 'width', '320')
    Config.set('graphics', 'height', '480')
    NosnoreApp().run()