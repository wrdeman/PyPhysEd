#!/opt/local/bin/python
"""
Module for opencv plotting graphs in opencv frame

"""
__author__ = 'wrdeman'
__version__ = '0/0'

import cv2
import numpy as np


class Plot:
    '''
    Will plot onto opencv image
    '''
    def __init__(self, video):
        self.origin = []
        self.video = video
        self.graph_data = np.array([])
        self.graph_axis = np.array([0, 1, 2, 2])
        self.max_loop = 1000

    def plot_points(self):
        '''
        find the points to plot
        '''
        self.features = self.video.features
        i = 0
        x_0 = 0
        y_0 = 0
        for temp in range(len(self.origin)-1):
            for x, y in np.float32(self.origin).reshape(-1, 2):
                x_0 = x
                y_0 = y
        for x, y in np.float32(self.features).reshape(-1, 2):
            if i == 0:
                L = np.sqrt((x-x_0)**2+(y-y_0)**2)
                theta = np.sin((y-y_0)/L)
                amp = y-y_0
        for x, y in np.float32(self.features).reshape(-1, 2):
            if i == 0:
                if len(self.graph_data) == 0:
                    self.graph_data = np.array([[0, amp, 0, theta, 0, x, y]])
                elif len(self.graph_data)<self.max_loop:
                    dtheta = (theta-self.graph_data[len(self.graph_data)-1, 4])\
                             /(len(self.graph_data)-\
                               self.graph_data[len(self.graph_data)-1, 0])
                    damp = (amp-self.graph_data[len(self.graph_data)-1, 2])\
                           /(len(self.graph_data)\
                             -self.graph_data[len(self.graph_data)-1, 0])
                    self.graph_data = np.append(self.graph_data,
                                              [[len(self.graph_data),
                                                amp,
                                                damp,
                                                theta,
                                                dtheta,
                                                x,
                                                y]]
                                              , 0)
                else:
                    dtheta = (theta-self.graph_data[len(self.graph_data)-1, 4])\
                             /(len(self.graph_data)\
                               -self.graph_data[len(self.graph_data)-1, 0])
                    damp = (amp-self.graph_data[len(self.graph_data)-1, 2])\
                           /(len(self.graph_data)\
                             -self.graph_data[len(self.graph_data)-1, 0])
                    self.graph_data = np.delete(self.graph_data, 0, 0)
                    self.graph_data = np.append(self.graph_data,
                                              [[len(self.graph_data),
                                                amp,
                                                damp,
                                                theta,
                                                dtheta,
                                                x,
                                                y]]
                                              , 0)
        i += 1


    def plot_data(self):        
        '''
        now plot the data onto the current frame
        '''
        self.current_frame = self.video.current_frame
        yy2, xx2 = self.current_frame.shape[:2]

        xx1 = 0
        yy1 = 0

        xx2 = int((xx2-xx1)/2)
        yy2 = int((yy2-yy1)/2)
        
        #opencv lengths of axis
        dx  =  (xx2+xx2*0.9)-xx2
        dy  =  yy2 - (yy2*0.1)
        
        #y-axis
        cv2.line(self.current_frame, 
                 (xx2, int(yy2*0.1)), 
                 (xx2, yy2), 
                 (255, 0, 0), 
                 1)
        #x-axis
        cv2.line(self.current_frame, 
                 (xx2, yy2), 
                 (int(xx2+xx2*0.9), yy2), 
                 (255, 0, 0), 
                 1)
        
        #xlabel x0,xly0
        self.xaxis("time", xx2, dx, yy2)
        self.yaxis("x", yy2, dy, xx2)




        xmax = np.amax(self.graph_data[:, self.graph_axis[0]])
        xmin = np.amin(self.graph_data[:, self.graph_axis[0]])

        ymax = np.amax(self.graph_data[:, self.graph_axis[1]])
        ymin = np.amin(self.graph_data[:, self.graph_axis[1]])

        pts = len(self.graph_data[:, self.graph_axis[0]])

        if pts > 1:
            for i in range(pts-1):
                xdat = self.graph_data[i, self.graph_axis[0]]
                ydat = self.graph_data[i, self.graph_axis[1]]
                x_cv1 = ((xdat-xmin)/(xmax-xmin))*dx+xx2
                y_cv1 = ((ydat-ymin)/(ymax-ymin))*dy+yy2*0.1
                xdat = self.graph_data[i+1, self.graph_axis[0]]
                ydat = self.graph_data[i+1, self.graph_axis[1]]
                x_cv2 = ((xdat-xmin)/(xmax-xmin))*dx+xx2
                y_cv2 = ((ydat-ymin)/(ymax-ymin))*dy+yy2*0.1
                cv2.line(self.current_frame,
                         (int(x_cv1), int(y_cv1)),
                         (int(x_cv2), int(y_cv2)),
                         (255, 255, 0),
                         1)

    def xaxis(self, string, x0, xLen, y0):
        '''
        sort out the xaxis
        '''
        cv2.putText(self.current_frame,
                    string,
                    (int(x0+(xLen/3)),
                     int(y0+40)),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (255, 0, 0)
                )

    def yaxis(self, string, y0, yLen, x0):
        '''
        sort out the y axis
        '''
        cv2.putText(self.current_frame,
                    string,
                    (int(x0-40),
                    int(y0*0.1+(y0/2))),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (255, 0, 0)
                )




