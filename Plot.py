#!/opt/local/bin/python
"""
Module for opencv plotting graphs in opencv frame

"""
__author__ = 'wrdeman'
__version__ = '0/0'

import sys
import cv2
import numpy as np
import Video

class Plot:
    def __init__(self,video):
        self.origin=[]
        self.video = video
        self.graphData=np.array([])
        self.graphAxis=np.array([0,1,2,2])
        self.max_loop=1000

    def plotPoints(self):
        self.features=self.video.features
        i=0
        x_0=0
        y_0=0
        for temp in range(len(self.origin)-1):
            for x,y in np.float32(self.origin).reshape(-1,2):
                x_0=x
                y_0=y
        for x, y in np.float32(self.features).reshape(-1, 2):
            if i==0:
                L=np.sqrt((x-x_0)**2+(y-y_0)**2)
                theta=np.sin((y-y_0)/L)
                amp=y-y_0
        for x, y in np.float32(self.features).reshape(-1, 2):
            if i==0:
                if len(self.graphData)==0:
                    self.graphData=np.array([[0,amp,0,theta,0,x,y]])
                elif len(self.graphData)<self.max_loop:
                    dtheta=(theta-self.graphData[len(self.graphData)-1,4])/(len(self.graphData)-self.graphData[len(self.graphData)-1,0])
                    damp=(amp-self.graphData[len(self.graphData)-1,2])/(len(self.graphData)-self.graphData[len(self.graphData)-1,0])
                    self.graphData=np.append(self.graphData,
                                              [[len(self.graphData),amp,damp,theta,dtheta,x,y]]
                                              ,0)
                else:
                    dtheta=(theta-self.graphData[len(self.graphData)-1,4])/(len(self.graphData)-self.graphData[len(self.graphData)-1,0])
                    damp=(amp-self.graphData[len(self.graphData)-1,2])/(len(self.graphData)-self.graphData[len(self.graphData)-1,0])
                    self.graphData=np.delete(self.graphData,0,0)
                    self.graphData=np.append(self.graphData,
                                              [[len(self.graphData),amp,damp,theta,dtheta,x,y]]
                                              ,0)
        i+=1


    def plotData(self):        
#opencv axis
        self.currentFrame=self.video.currentFrame
        yy2,xx2=self.currentFrame.shape[:2]

        xx1=0
        yy1=0

        xx2=int((xx2-xx1)/2)
        yy2=int((yy2-yy1)/2)
        
        #opencv lengths of axis
        dx = (xx2+xx2*0.9)-xx2
        dy = yy2 - (yy2*0.1)

        cv2.line(self.currentFrame,(xx2,int(yy2*0.1)),(xx2,yy2),(255,0,0),1)
        cv2.line(self.currentFrame,(xx2,yy2),(int(xx2+xx2*0.9),yy2),(255,0,0),1)

        xmax = np.amax(self.graphData[:,self.graphAxis[0]])
        xmin = np.amin(self.graphData[:,self.graphAxis[0]])

        ymax = np.amax(self.graphData[:,self.graphAxis[1]])
        ymin = np.amin(self.graphData[:,self.graphAxis[1]])

        pts = len(self.graphData[:,self.graphAxis[0]])

        if pts > 1:
            for i in range(pts-1):
                xdat = self.graphData[i,self.graphAxis[0]]
                ydat = self.graphData[i,self.graphAxis[1]]
                x_cv1 = ((xdat-xmin)/(xmax-xmin))*dx+xx2
                y_cv1 = ((ydat-ymin)/(ymax-ymin))*dy+yy2*0.1
                xdat = self.graphData[i+1,self.graphAxis[0]]
                ydat = self.graphData[i+1,self.graphAxis[1]]
                x_cv2 = ((xdat-xmin)/(xmax-xmin))*dx+xx2
                y_cv2 = ((ydat-ymin)/(ymax-ymin))*dy+yy2*0.1
                cv2.line(self.currentFrame,(int(x_cv1),int(y_cv1)),(int(x_cv2),int(y_cv2)),(255,255,0),1)




