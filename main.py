import cv2 as cv
import numpy as np
import os
from time import time
from Window_Capture import WindowCapture
from vision import findClickPositions

#WindowCapture.list_window_names()
#exit()

#create object
wincap = WindowCapture('Diablo II: Resurrected')

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()

    #cv.imshow('Computer Vision', screenshot) #just showing us the raw screenshot, not needed anymore
    findClickPositions('zombie_1.jpg', screenshot, 0.5, 'rectangles')

    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #'pressing "Q" will exit
    #Waits 1ms every loop
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')