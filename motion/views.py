from kivy.app import App

from motion.widgets import MainApp


class PhysedApp(App):
    def build(self):
        return MainApp()
