from kivy.app import App

from .widgets import MainApp


class PhysedApp(App):
    def build(self):
        return MainApp()
