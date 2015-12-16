#!/opt/local/bin/python
"""
Module for opencv tracking of objects

"""
__author__ = 'wrdeman'
__version__ = '0/0'

import numpy as np

from kivy.clock import Clock
from kivy.logger import Logger
from kivy.graphics.texture import Texture
from kivy.core.camera import CameraBase as CoreCamera

from motion.plot import Plot

try:
    import opencv as cv
    import opencv.highgui as hg
except ImportError:
    import cv2

    class Hg(object):
        '''
        On OSX, not only are the import names different, but the API also
        differs. There is no module called 'highgui' but the names are directly
        available in the 'cv' module. Some of them even have a different
        names.
        Therefore we use this proxy object.
        '''
        def __getattr__(self, attr):
            if attr.startswith('cv2'):
                attr = attr[2:]
                got = getattr(cv, attr)
                return got
    hg = Hg()


class MyCamera(CoreCamera):
    def __init__(self, *args, **kwargs):
        self._device = None
        super(MyCamera, self).__init__(*args, **kwargs)
        self.features = []
        self.origin = []

        self.current_frame = np.array([])
        self.previous_frame = np.array([])
        self.lkp_def = ([50, 100, 50, 0.1, 0.0])
        self.fp_def = ([500, 0.001, 7, 7])
        self.lk_params = dict(
            winSize=(self.lkp_def[0], self.lkp_def[0]),
            maxLevel=self.lkp_def[1],
            criteria=(
                cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS,
                self.lkp_def[2], self.lkp_def[3]
            )
        )

        self.feature_params = dict(
            maxCorners=self.fp_def[0],
            qualityLevel=self.fp_def[1],
            minDistance=self.fp_def[2],
            blockSize=self.fp_def[3]
        )
        self.plot = Plot(self)

    def init_camera(self):
        # create the device
        self._device = cv2.VideoCapture(self._index)

        # Set preferred resolution
        self._device.set(
            3,
            self.resolution[0]
        )
        self._device.set(
            4,
            self.resolution[1]
        )

        # and get frame to check if it's ok

        ret, frame = self._device.read()

        # Just set the resolution to the frame we just got, but don't use
        # self.resolution for that as that would cause an infinite recursion
        # with self.init_camera (but slowly as we'd have to always get a
        # frame).
        height, width, _ = frame.shape
        self._resolution = (int(width), int(height))

        # get fps
        self.fps = self._device.get(5)
        if self.fps <= 0:
            self.fps = 1 / 30.

        if not self.stopped:
            self.start()

    def _update(self, dt):
        if self.stopped:
            return
        if self._texture is None:
            # Create the texture
            self._texture = Texture.create(self._resolution)
            self._texture.flip_vertical()
            self.dispatch('on_load')
        try:
            ret, frame = self._device.read()
            self.get_current_frame(ret, frame)

            self._format = 'bgr'
            try:
                self._buffer = self.current_frame.imageData
            except AttributeError:
                # On OSX there is no imageData attribute but a tostring()
                # method.
                self._buffer = self.current_frame.tostring()
                self._copy_to_gpu()
            self.previous_frame = self.current_frame
        except:
            Logger.exception('OpenCV: Couldn\'t get image from Camera')

    def get_current_frame(self, ret, frame):
        """
        capture frame and reverse RBG BGR and return opencv image
        """
        if ret:
            self.current_frame = cv2.cvtColor(
                frame, cv2.COLOR_BGR2RGB
            )
            if self.features != []:
                self.track_points()
                self.draw_points()
                self.plot.plot_points()
                self.plot.plot_data()
        else:
            self.current_frame = None

    def kivy_to_cv(self, pos, video_params):
        image_x = video_params['width']
        image_y = video_params['height']

        height, width = self.current_frame.shape[:2]

        init_image_x = 0
        init_image_y = 640

        x = int(width*(pos['x']-init_image_x)/image_x)
        y = int(height*(init_image_y-pos['y'])/image_y)

        return x, y

    def add_point(self, pos, video_params):
        """
        add a point
        switch between opencv coordinates and PyQt

        """

        if isinstance(self.current_frame, np.ndarray):
            img_event = self.current_frame

            img_event = cv2.cvtColor(img_event, cv2.COLOR_BGR2RGB)
            xscaled, yscaled = self.kivy_to_cv(pos, video_params)

            if xscaled > 0 and yscaled > 0:
                gray = cv2.cvtColor(img_event, cv2.COLOR_RGB2GRAY)
                mask = np.zeros_like(gray)
                mask[:] = 255
                cv2.circle(mask, (xscaled, yscaled), 100, 1, -1)
                points = cv2.goodFeaturesToTrack(
                    gray,
                    mask=mask,
                    **self.feature_params
                )

                if points is not None:
                    for x, y in np.float32(points).reshape(-1, 2):
                        circ = ((x-xscaled)**2+(y-yscaled)**2)**0.5
                        if circ < 50:
                            self.features.append(
                                [(int(x), int(y))]
                            )

                            cv2.circle(
                                img_event,
                                (x, y),
                                10,
                                (255, 0, 0),
                                -1
                            )
                            if (len(self.features) != 0):
                                for x, y in np.float32(
                                        self.features
                                ).reshape(-1, 2):
                                    cv2.circle(
                                        img_event,
                                        (x, y),
                                        10,
                                        (255, 255, 0),
                                        -1
                                    )
                            break

    def draw_points(self):
        '''
        draw points on windows
        '''
        new_tracks = []
        p0 = np.float32([tr[-1] for tr in self.features]).reshape(-1, 1, 2)
        for tr, (x, y) in zip(self.features, p0.reshape(-1, 2)):
            if len(tr) > len(self.features):
                del tr[0]
            new_tracks.append(tr)
            cv2.circle(self.current_frame, (x, y), 10, (255, 0, 0), -1)
        self.features = new_tracks

    def track_points(self):
        '''
        track points in self.features and draw circle
        '''
        p0 = np.float32(
            [tr[-1] for tr in self.features]
        ).reshape(-1, 1, 2)
        self.features, st, err = cv2.calcOpticalFlowPyrLK(
            self.previous_frame,
            self.current_frame,
            p0,
            None,
            **self.lk_params
        )

    def start(self):
        super(MyCamera, self).start()
        Clock.unschedule(self._update)
        Clock.schedule_interval(self._update, self.fps)

    def stop(self):
        super(MyCamera, self).stop()
        Clock.unschedule(self._update)
