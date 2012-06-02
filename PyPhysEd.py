#!/usr/bin/python
'''Program to track motion of pendulum

'''
__author__ = 'Simon Osborne'
__version__ = '0.0'

import sys
from PyQt4 import QtGui, QtCore, Qt
import cv2
import PyQt4.Qwt5 as Qwt
import numpy as np
from test_ui import Ui_MainWindow
from my_pop import Ui_Form
from os.path import isfile, splitext

class Popup(QtGui.QMainWindow):
    '''Pop up window to define tracking parameters'''
    def __init__(self,lkp_in,fp_in):
        QtGui.QWidget.__init__(self)
        self.uipop=Ui_Form()
        self.uipop.setupUi(self)
        self.lkp_def=lkp_in
        self.fp_def=fp_in
        self.popTable()       
        QtCore.QObject.connect(self.uipop.fp_Table,
                               QtCore.SIGNAL("cellChanged(int, int)"),
                               self.new_fp)
        QtCore.QObject.connect(self.uipop.lkp_Table,
                               QtCore.SIGNAL("cellChanged(int, int)"),
                               self.new_lkp)
        QtCore.QObject.connect(self.uipop.pushClose,
                               QtCore.SIGNAL("clicked()"),
                               self.close)

    def popTable(self):
        for i in range(len(self.lkp_def)):
            item=QtGui.QTableWidgetItem(QtCore.QString(str(self.lkp_def[i])))
            self.uipop.lkp_Table.setItem(i,0,item)
        for i in range(len(self.fp_def)):
            item=QtGui.QTableWidgetItem(QtCore.QString(str(self.fp_def[i])))
            self.uipop.fp_Table.setItem(i,0,item)

    def new_lkp(self):
        for i in range(len(self.lkp_def)):
            if i<2:
                self.lkp_def[i]=int(self.uipop.lkp_Table.item(i, 0).text())
            else:
                self.lkp_def[i]=float(self.uipop.lkp_Table.item(i, 0).text())

    def new_fp(self):
        for i in range(len(self.fp_def)):
            self.fp_def[i]=int(self.uipop.fp_Table.item(i, 0).text())
            self.fp_def[1]=float(self.uipop.fp_Table.item(1, 0).text())

class Example(QtGui.QMainWindow):   


    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()        
        self.ui.setupUi(self)
        self.initUI()
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.playCapture)
        self._timer.start(27)  
        QtCore.QObject.connect(self.ui.actionFile,
                               QtCore.SIGNAL("triggered()"), 
                               self.fileDialog)
        QtCore.QObject.connect(self.ui.actionCam,
                               QtCore.SIGNAL("triggered()"), 
                               self.camDialog)
        QtCore.QObject.connect(self.ui.actionTracking,
                               QtCore.SIGNAL("triggered()"), 
                               self.paramsDialog)
        QtCore.QObject.connect(self.ui.actionUpdate,
                               QtCore.SIGNAL("triggered()"), 
                               self.paramsUpdate)
        QtCore.QObject.connect(self.ui.pushStart,
                               QtCore.SIGNAL("clicked()"), 
                               self.playOK)
        QtCore.QObject.connect(self.ui.actionQuit,
                               QtCore.SIGNAL("triggered()"),
                               QtCore.QCoreApplication.instance().quit)
        #connections for subplot 1-x
        QtCore.QObject.connect(self.ui.actionTime,
                               QtCore.SIGNAL("triggered()"),
                               lambda x1="t": self.changex1(x1))
        QtCore.QObject.connect(self.ui.actionAmp,
                               QtCore.SIGNAL("triggered()"), 
                               lambda x1="a": self.changex1(x1))
        QtCore.QObject.connect(self.ui.actionD_amp_dt,
                               QtCore.SIGNAL("triggered()"),
                               lambda x1="da": self.changex1(x1))
        QtCore.QObject.connect(self.ui.actionTheta,
                               QtCore.SIGNAL("triggered()"), 
                               lambda x1="th": self.changex1(x1))
        QtCore.QObject.connect(self.ui.actionD_theta_dt,
                               QtCore.SIGNAL("triggered()"),
                               lambda x1="dth": self.changex1(x1))
        QtCore.QObject.connect(self.ui.actionX,
                               QtCore.SIGNAL("triggered()"), 
                               lambda x1="x": self.changex1(x1))
        QtCore.QObject.connect(self.ui.actionY,
                               QtCore.SIGNAL("triggered()"), 
                               lambda x1="y": self.changex1(x1))
        #connections for subplot 1-y
        QtCore.QObject.connect(self.ui.actionTime_2,
                               QtCore.SIGNAL("triggered()"),
                               lambda y1="t": self.changey1(y1))
        QtCore.QObject.connect(self.ui.actionAmp_2,
                               QtCore.SIGNAL("triggered()"), 
                               lambda y1="a": self.changey1(y1))
        QtCore.QObject.connect(self.ui.actionD_amp_dt_2,
                               QtCore.SIGNAL("triggered()"),
                               lambda y1="da": self.changey1(y1))
        QtCore.QObject.connect(self.ui.actionTheta_2,
                               QtCore.SIGNAL("triggered()"), 
                               lambda y1="th": self.changey1(y1))
        QtCore.QObject.connect(self.ui.actionD_theta_dt_2,
                               QtCore.SIGNAL("triggered()"),
                               lambda y1="dth": self.changey1(y1))
        QtCore.QObject.connect(self.ui.actionX_2,
                               QtCore.SIGNAL("triggered()"), 
                               lambda y1="x": self.changey1(y1))
        QtCore.QObject.connect(self.ui.actionY_2,
                               QtCore.SIGNAL("triggered()"), 
                               lambda y1="y": self.changey1(y1))
        #connections for subplot 2-x 
        QtCore.QObject.connect(self.ui.actionRemove,
                               QtCore.SIGNAL("triggered()"), 
                               self.remove2)
        QtCore.QObject.connect(self.ui.actionTime_3,
                               QtCore.SIGNAL("triggered()"),
                               lambda x2="t": self.changex2(x2))
        QtCore.QObject.connect(self.ui.actionAmp_3,
                               QtCore.SIGNAL("triggered()"), 
                               lambda x2="a": self.changex2(x2))
        QtCore.QObject.connect(self.ui.actionD_amp_dt_3,
                               QtCore.SIGNAL("triggered()"),
                               lambda x2="da": self.changex2(x2))
        QtCore.QObject.connect(self.ui.actionTheta_3,
                               QtCore.SIGNAL("triggered()"), 
                               lambda x2="th": self.changex2(x2))
        QtCore.QObject.connect(self.ui.actionD_theta_dt_3,
                               QtCore.SIGNAL("triggered()"),
                               lambda x2="dth": self.changex2(x2))
        QtCore.QObject.connect(self.ui.actionX_3,
                               QtCore.SIGNAL("triggered()"), 
                               lambda x2="x": self.changex2(x2))
        QtCore.QObject.connect(self.ui.actionY_3,
                               QtCore.SIGNAL("triggered()"), 
                               lambda x2="y": self.changex2(x2))
        #connections for subplot 2-y 
        QtCore.QObject.connect(self.ui.actionTime_4,
                               QtCore.SIGNAL("triggered()"),
                               lambda y2="t": self.changey2(y2))
        QtCore.QObject.connect(self.ui.actionAmp_4,
                               QtCore.SIGNAL("triggered()"), 
                               lambda y2="a": self.changey2(y2))
        QtCore.QObject.connect(self.ui.actionD_amp_dt_4,
                               QtCore.SIGNAL("triggered()"),
                               lambda y2="da": self.changey2(y2))
        QtCore.QObject.connect(self.ui.actionTheta_4,
                               QtCore.SIGNAL("triggered()"), 
                               lambda y2="th": self.changey2(y2))
        QtCore.QObject.connect(self.ui.actionD_theta_dt_4,
                               QtCore.SIGNAL("triggered()"),
                               lambda y2="dth": self.changey2(y2))
        QtCore.QObject.connect(self.ui.actionX_4,
                               QtCore.SIGNAL("triggered()"), 
                               lambda y2="x": self.changey2(y2))
        QtCore.QObject.connect(self.ui.actionY_4,
                               QtCore.SIGNAL("triggered()"), 
                               lambda y2="y": self.changey2(y2))
        
    def initUI(self):      
        self.loop=0
        self.features=[]
        self.origin=[]
        self.graph_data = np.array([])         # define arrays
        self.graph_axis=np.array([0,1,2,2])
        self.RpreviousImage=np.array([])
        self.captureGot=False
        self.captureGo=False
        self.subplots=1
        self.max_loop=200
        self.remove2()
        self.change1=False
        self.change2=False
        self.axis_params=[('t',0,'time'),
                          ('a',1,'amplitude'),
                          ('da',2,'d(Amp)/dt'),
                          ('th',3,'theta'),
                          ('dth',4,'d(theta)/dt'),
                          ('x',5,'x pos'),
                          ('y',6,'y pos')]
        self.plt1 = Qwt.QwtPlotCurve("Data")
        self.plt1.setPen(Qt.QPen(Qt.Qt.green, 1))
        self.ui.qwtPlot1.setAxisTitle(Qwt.QwtPlot.xBottom, 'time')
        self.ui.qwtPlot1.setAxisTitle(Qwt.QwtPlot.yLeft, 'amplitude')
        self.ui.qwtPlot1.show()               
        self.plt2 = Qwt.QwtPlotCurve("Data")
        self.plt2.setPen(Qt.QPen(Qt.Qt.blue, 1))
        self.ui.qwtPlot2.show()               
        self.lkp_def=([50,100,50,0.1,0.0])
        self.fp_def=([500,0.001,7,7])
        self.lk_params = dict( winSize  = (self.lkp_def[0], self.lkp_def[0]), 
                               maxLevel = self.lkp_def[1], 
                               criteria = (cv2.TERM_CRITERIA_COUNT | 
                                           cv2.TERM_CRITERIA_EPS, 
                                           self.lkp_def[2], self.lkp_def[3]),
                               derivLambda = self.lkp_def[4] )  
        self.feature_params = dict( maxCorners = self.fp_def[0], 
                                    qualityLevel = self.fp_def[1],
                                    minDistance = self.fp_def[2],
                                    blockSize = self.fp_def[3] )
   
    def fileDialog(self):
        openfile=QtGui.QFileDialog()
        openfile.setOption(QtGui.QFileDialog.DontUseNativeDialog)
        fname=openfile.getOpenFileName(self,'Open file','.')       
        if isfile(fname):
            self.capture = cv2.VideoCapture(str(fname))
            self.captureGot=True

    def save(self):
        save = QtGui.QFileDialog()
        save.setOption(QtGui.QFileDialog.DontUseNativeDialog)
        fname=save.getOpenFileName(self,'Open file','.')
        time=np.linspace(0,(self.i_time+self.init_size)*self.time_step,
                         (self.i_time+self.init_size))
        temp=np.rot90(np.vstack((time,self.data[self.i_time:self.i_time+2000])))
        np.savetxt(str(fname),temp)
        temp=np.rot90(np.vstack((self.freq,np.real(self.psd))))
        path,ext=os.path.splitext(str(fname))
        print 'path = ',str(path),' ext = ',str(ext),' new = ',str(path)+'_fft'+str(ext)
        np.savetxt(str(path)+'_fft'+str(ext),temp)

    def camDialog(self):
        self.capture = cv2.VideoCapture(0)
        self.captureGot=True

    def playOK(self):
        if self.captureGo==False:
            self.captureGo=True
            self.ui.pushStart.setText('Stop')
        else: 
            self.captureGo=False
            self.ui.pushStart.setText('Start')


    def paramsDialog(self):
        self.pop=Popup(self.lkp_def,self.fp_def)
        self.pop.show()

#not very elegent or pythonic
    def paramsUpdate(self):
        for i in range(len(self.pop.lkp_def)):
            self.lkp_def[i]=self.pop.lkp_def[i]
        for i in range(len(self.fp_def)):
            self.fp_def[i]=self.pop.fp_def[i]       

    def remove2(self):
        self.subplots=1
        w=self.ui.splitter.height()
        self.ui.splitter.setSizes([w,0])
        self.graph_axis[2]=-1
        self.graph_axis[3]=-1

    def add2(self):
        if self.graph_axis[2]!=-1 and self.graph_axis[3]!=-1:
            self.subplots=2
            w=self.ui.splitter.height()
            self.ui.splitter.setSizes([w/2,w/2])
            self.plotData()

    def changex1(self, axis):
        for qlab,i,labtxt in self.axis_params:
            if axis==qlab:
                self.graph_axis[i]=i
                self.ui.qwtPlot1.setAxisTitle(Qwt.QwtPlot.xBottom,labtxt)
        self.change1=True
        self.ui.qwtPlot1.show()               
        self.plotData()

    def changey1(self, axis):
        for qlab,i,labtxt in self.axis_params:
            if axis==qlab:
                self.graph_axis[i]=i
                self.ui.qwtPlot1.setAxisTitle(Qwt.QwtPlot.yLeft,labtxt)
        self.change1=True
        self.ui.qwtPlot1.show()               
        self.plotData()

    def changex2(self, axis):
        for qlab,i,labtxt in self.axis_params:
            if axis==qlab:
                self.graph_axis[i]=i
                self.ui.qwtPlot2.setAxisTitle(Qwt.QwtPlot.xBottom,labtxt)
        self.change2=True
        self.ui.qwtPlot2.show()               
        self.add2()

    def changey2(self, axis):
        for qlab,i,labtxt in self.axis_params:
            if axis==qlab:
                self.graph_axis[i]=i
                self.ui.qwtPlot2.setAxisTitle(Qwt.QwtPlot.yLeft,labtxt)
        self.change2=True
        self.ui.qwtPlot2.show()               
        self.add2()

    def playCapture(self):
        if self.captureGo==True and self.captureGot==True:
            self.ret, self.frame=self.capture.read()
            currentImage=self.frame
            if(self.ret!=False):
                RcurrentImage=cv2.cvtColor(currentImage,cv2.COLOR_BGR2RGB)
                if (len(self.RpreviousImage)!=0) and len(self.features)!=0:
                    TRcurrentImage=self.trackPoint(RcurrentImage,self.RpreviousImage)
                    self.plotPoints()
                    self.loop+=1
                else:
                    TRcurrentImage=RcurrentImage
                self.Qimg=self.convertImage(TRcurrentImage)
                self.ui.video_lbl.setPixmap(self.Qimg)
                self.ui.video_lbl.setScaledContents(True)           
                self.RpreviousImage=RcurrentImage
                if self.loop==0 and self.ui.pausefirstBox.checkState()==2:
                    self.captureGo=False
                    self.ui.pushStart.setText('Start')
                else:
                    self.update()        
                        
    def trackPoint(self,cvImage,cvImage_prev):
        #track points in self.features and draw circle
        p0 = np.float32([tr[-1] for tr in self.features]).reshape(-1, 1, 2)
        self.features, st,err=cv2.calcOpticalFlowPyrLK(cvImage_prev,
                                                       cvImage,
                                                       p0,
                                                       None, 
                                                       **self.lk_params)
        new_tracks=[]
        for tr, (x, y) in zip(self.features, p0.reshape(-1, 2)):
            if len(tr) > len(self.features):
                del tr[0]
            new_tracks.append(tr)
            cv2.circle(cvImage, (x, y), 10, (255, 0, 0), -1)
        self.features = new_tracks
        #draww origin
        p0 = np.float32([tr[-1] for tr in self.origin]).reshape(-1, 1, 2)
        for tr, (x, y) in zip(self.origin, p0.reshape(-1, 2)):
            cv2.circle(cvImage, (x, y), 10, (255, 255, 0), -1)      
        return cvImage

    def plotPoints(self):
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
                if self.loop==0:
                    self.graph_data=np.array([[self.loop,amp,0,theta,0,x,y]])
                elif self.loop<self.max_loop:
                    dtheta=(theta-self.graph_data[len(self.graph_data)-1,4])/(self.loop-self.graph_data[len(self.graph_data)-1,0])
                    damp=(amp-self.graph_data[len(self.graph_data)-1,2])/(self.loop-self.graph_data[len(self.graph_data)-1,0])
                    self.graph_data=np.append(self.graph_data,
                                              [[self.loop,amp,damp,theta,dtheta,x,y]]
                                              ,0)
                else:
                    dtheta=(theta-self.graph_data[len(self.graph_data)-1,4])/(self.loop-self.graph_data[len(self.graph_data)-1,0])
                    damp=(amp-self.graph_data[len(self.graph_data)-1,2])/(self.loop-self.graph_data[len(self.graph_data)-1,0])
                    self.graph_data=np.delete(self.graph_data,0,0)
                    self.graph_data=np.append(self.graph_data,
                                              [[self.loop,amp,damp,theta,dtheta,x,y]]
                                              ,0)
        i+=1
        self.plotData()

    def plotData(self):
            self.plt1.setData(self.graph_data[:,self.graph_axis[0]],
                              self.graph_data[:,self.graph_axis[1]])
            self.plt1.attach(self.ui.qwtPlot1)
            self.ui.qwtPlot1.replot()                
            self.plt2.setData(self.graph_data[:,self.graph_axis[2]],
                              self.graph_data[:,self.graph_axis[3]])
            self.plt2.attach(self.ui.qwtPlot2)
            self.ui.qwtPlot2.replot()                

    def convertImage(self,cvImage):
        height,width=cvImage.shape[:2]
        self.img=QtGui.QImage(cvImage,
                              width,
                              height,
                              QtGui.QImage.Format_RGB888)
        self.img=QtGui.QPixmap.fromImage(self.img)              
        return self.img

    def mousePressEvent(self, event):
        self.lastPos=QtCore.QPoint(event.pos())
        video_params=self.ui.video_lbl.geometry()
        self.image_x=video_params.right()
        self.image_y=video_params.bottom()
        self.init_image_x=video_params.left()
        self.init_image_y=video_params.top()
        if self.ret==True:
            img_event=self.frame
            # x and y position of mouseclick relative to PyQt
            xpos=self.lastPos.x()  
            ypos=self.lastPos.y()
            if ((xpos-self.init_image_x)<self.image_x and 
                (ypos-self.init_image_y)<self.image_y):
                img_event=cv2.cvtColor(img_event,cv2.COLOR_BGR2RGB) 
                height,width=img_event.shape[:2]
                # scale PyQt coordinates to OpenCV
                xscaled=int(width*(xpos-self.init_image_x)/self.image_x)  
                yscaled=int(height*(ypos-self.init_image_y)/self.image_y)
                term = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
                gray = cv2.cvtColor(img_event, cv2.COLOR_RGB2GRAY)
                mask = np.zeros_like(gray)
                mask[:] = 255
                cv2.circle(mask, (xscaled, yscaled), 100, 1, -1)
                p = cv2.goodFeaturesToTrack(gray, 
                                            mask = mask, 
                                            **self.feature_params)
                add_point=False
                if (event.button() == QtCore.Qt.LeftButton 
                    and QtGui.QApplication.keyboardModifiers()==QtCore.Qt.ShiftModifier 
                    and len(self.origin)==0):
                    if p is not None:
                        for x, y in np.float32(p).reshape(-1, 2):
                            if add_point==False:
                                circ=((x-xscaled)**2+(y-yscaled)**2)**0.5
                                if circ<50:
                                    self.origin.append([(int(x),int(y))])
                                    add_point=True
                                    cv2.circle(img_event, 
                                               (x, y), 
                                               10, 
                                               (255, 255, 0), 
                                               -1)
                                    if (len(self.features)!=0):
                                        for x, y in np.float32(self.features).reshape(-1, 2):
                                            cv2.circle(img_event, 
                                                       (x, y), 
                                                       10, 
                                                       (255, 0, 0), 
                                                       -1)
                                    self.Qimg=self.convertImage(img_event)
                                    self.ui.video_lbl.setPixmap(self.Qimg)
                                    self.ui.video_lbl.setScaledContents(True) 

                else:
                    if p is not None:
                        for x, y in np.float32(p).reshape(-1, 2):
                            if add_point==False:
                                circ=((x-xscaled)**2+(y-yscaled)**2)**0.5
                                if circ<50:
                                    self.features.append([(int(x),int(y))])
                                    add_point=True
                                    cv2.circle(img_event, (x, y), 10, (255, 0, 0), -1)
                                    if (len(self.origin)!=0):
                                        for x, y in np.float32(self.origin).reshape(-1, 2):
                                            cv2.circle(img_event, 
                                                       (x, y), 
                                                       10, 
                                                       (255, 255, 0), 
                                                       -1)
                                    self.Qimg=self.convertImage(img_event)
                                    self.ui.video_lbl.setPixmap(self.Qimg)
                                    self.ui.video_lbl.setScaledContents(True)           

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()                        
        if e.key() == QtCore.Qt.Key_Backspace:
            self.features.pop(len(self.features)-1)
        if e.key() == QtCore.Qt.Key_Tab:
            self.origin.pop(0)
           

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
