from kivy.app import App
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel


class Panel(TabbedPanel):
    pass


class NosnoreApp(App):
    def build(self):
        return Panel()


if __name__ == '__main__':
    Config.set('graphics', 'width', '320')
    Config.set('graphics', 'height', '480')
    NosnoreApp().run()