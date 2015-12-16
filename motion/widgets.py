from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.camera import Camera

from motion.video import MyCamera


class MainApp(BoxLayout):
    pass


class PlayButton(ToggleButton):
    def __init__(self, *args, **kwargs):
        super(PlayButton, self).__init__(*args, **kwargs)
        self.state = 'down'
        self.bind(on_press=self.button_pressed)
        self.bind(on_release=self.button_pressed)

    def button_pressed(self, button):
        ctl = self.parent.ids['camera_id']
        if self.state == 'down':
            self.state = 'normal'
            ctl.play = True
        else:
            self.state = 'down'
            ctl.play = False


class CameraWidget(Camera):
    def __init__(self, *args, **kwargs):
        super(CameraWidget, self).__init__(*args, **kwargs)
        # self.play = True

    def _on_index(self, *largs):
        self._camera = None
        if self.index < 0:
            return
        if self.resolution[0] < 0 or self.resolution[1] < 0:
            return
        self._camera = MyCamera(
            index=self.index, resolution=self.resolution, stopped=True
        )
        self._camera.bind(on_load=self._camera_loaded)
        if self.play:
            self._camera.start()
            self._camera.bind(on_texture=self.on_tex)

    def on_touch_down(self, touch):
        image_size = {
            'width': self.width,
            'height': self.height
        }
        pos = {'x': touch.pos[0], 'y': touch.pos[1]}
        self._camera.add_point(pos, image_size)
