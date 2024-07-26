import cv2 as cv
import numpy as np
import os
from time import time
from Window_Capture import WindowCapture
from vision import Vision

#WindowCapture.list_window_names()
#exit()

#create object
wincap = WindowCapture('Diablo II: Resurrected')
#Init Vision Class; because it not gonna change inside main loop:
Vision_zombie = Vision('zombie_1.jpg')

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()

    #displays the processed img
    Vision_zombie.find(screenshot, 0.5, 'rectangles')

    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #'pressing "Q" will exit
    #Waits 1ms every loop
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')