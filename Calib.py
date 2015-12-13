#!/opt/local/bin/python
"""
Module to calibrate the dimension of the plane of motion
Will use a chess board.
"""
__author__ = 'wrdeman'
__version__ = '0/0'

import cv2
import numpy as np

class Calib():
    def __init__(self):
        1

    def calibDists(self,img):
        self.img = img
        i=4
        j=4
        found=False
        while (not found):
            while(not found):
                pattern_size = (i, j)
                pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
                pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
                square_size=2
                pattern_points *= square_size

                obj_points = []
                img_points = []
                h, w = 0, 0
                h, w = self.img.shape[:2]
                found, corners = cv2.findChessboardCorners(self.img, pattern_size)
                if found:
                    term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
                    cv2.cornerSubPix(self.img, corners, (5, 5), (-1, -1), term)
                    vis = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
                    cv2.drawChessboardCorners(vis, pattern_size, corners, found)
                j+=1
            i+=1

        count=0
        distArray=[]
        for x, y in np.float32(corners).reshape(-1, 2):
            if count != 0:
                if abs(x_old-x)<5:
                    distArray.append(y-y_old)
                if abs(y_old-y)<5:
                    distArray.append(x-x_old)
            x_old=x
            y_old=y
            count=+1

        if len(distArray)==0:
            return 0
        else:
            return np.mean(distArray)

    def showImage():
        imshow(img)
        
