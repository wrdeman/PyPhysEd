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
        self.rawPoints = []
        self.video = video
        self.graphData=np.array([])
        self.graphAxis=np.array([0,1,2,2])
        self.max_loop=1000

    def plotRawPoints(self):
        '''
        an array containing the raw points (x,y) of the first tracked point
        '''
        self.features=self.video.features
        dt = self.video.dt
        count=0
        for x, y in np.float32(self.features).reshape(-1, 2):
            if count == 0:
                self.rawPoints.append([x,y,dt])

    def plotPoints(self):
        '''
        use rawPoints to generate points for plotting
        '''
        self.plotRawPoints()
        self.graphData=[]
        x_0=0
        y_0=0
        totalTime=0            
        if len(self.video.origin)  != 0: 
    #        for temp in range(len(self.video.origin)-1):
            for x,y in np.float32(self.video.origin).reshape(-1,2):
                x_0=x
                y_0=y

        for index, points in enumerate(self.rawPoints):
            time=points[2]
            x=points[0]
            y=points[1]
            
            theta=np.arctan((y-y_0)/(x-x_0))
            amp=x-x_0
            
            if index==0:
                self.graphData=np.array([[totalTime,amp,0,theta,0,x,y]])
            elif len(self.graphData)<self.max_loop:
                totalTime +=time
                dtheta=(theta-thetaLast)/(totalTime-timeLast)
                damp=(amp-ampLast)/(totalTime-timeLast)
                self.graphData=np.vstack((self.graphData,
                                         [totalTime,amp,damp,theta,dtheta,x,y]))
            else:
                totalTime += time
                dtheta=(theta-thetaLast)/(totalTime-timeLast)
                damp=(amp-ampLast)/(totalTime-timeLast)
                self.graphData=np.delete(self.graphData,0,0)
                self.graphData=np.vstack((self.graphData,
                                         [totalTime,amp,damp,theta,dtheta,x,y]))
            ampLast = amp
            thetaLast = theta
            timeLast=totalTime

    def plotData(self,xInt,yInt):        
        #opencv axis
        self.currentFrame=self.video.currentFrame

        xmax = np.amax(self.graphData[:,xInt])
        xmin = np.amin(self.graphData[:,xInt])

        ymax = np.amax(self.graphData[:,yInt])
        ymin = np.amin(self.graphData[:,yInt])

        #size of the opencv frame
        yy2,xx2=self.currentFrame.shape[:2]
        #size of half the opencv frame
        xx2=int((xx2)/2)
        yy2=int((yy2)/2)
        
        #opencv lengths of axis
        dx = (xx2*0.9)
        dy = (yy2*0.9)
        
        #y-axis
        cv2.line(self.currentFrame,(xx2,int(yy2*0.1)),(xx2,yy2),(255,0,0),1)
        #x-axis
        # i want the x axis to intercept the y at x=0
        if ymin*ymax>0:
            cv2.line(self.currentFrame,(xx2,yy2),(int(xx2+xx2*0.9),yy2),(255,0,0),1)
        else:
            adYInt = int(yy2 - dy*abs(ymin/(ymax-ymin)))
            cv2.line(self.currentFrame,(xx2,adYInt),(int(xx2+xx2*0.9),adYInt),(255,0,0),1)

        #xlabel x0,xly0
        axisLabels=["time","A","dA/dt","theta","d(theta)/dt","x","y"]
        
        self.xaxis(axisLabels[xInt],xx2,dx,yy2)
        self.yaxis(axisLabels[yInt],yy2,dy,xx2)

        pts = len(self.graphData[:,yInt])

        if pts > 1:
            for i in range(pts-1):
                xdat = self.graphData[i,xInt]
                ydat = self.graphData[i,yInt]
                x_cv1 = ((xdat-xmin)/(xmax-xmin))*dx+xx2
                y_cv1 = ((ydat-ymin)/(ymax-ymin))*dy+yy2*0.1
                xdat = self.graphData[i+1,xInt]
                ydat = self.graphData[i+1,yInt]
                x_cv2 = ((xdat-xmin)/(xmax-xmin))*dx+xx2
                y_cv2 = ((ydat-ymin)/(ymax-ymin))*dy+yy2*0.1
                cv2.line(self.currentFrame,(int(x_cv1),int(y_cv1)),(int(x_cv2),int(y_cv2)),(255,255,0),1)

    def xaxis(self,string,x0,xLen,y0):
        cv2.putText(self.currentFrame,
                    string,
                    (int(x0+(xLen/3)),
                     int(y0+40)),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (255,0,0)
                )

    def yaxis(self,string,y0,yLen,x0):
        cv2.putText(self.currentFrame,
                    string,
                    (int(x0-40),
                    int(y0*0.1+(y0/2))),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (255,0,0)
                )




