import cv2 as cv
import numpy as np
import os
from time import time
from Window_Capture import WindowCapture
from vision import Vision

#WindowCapture.list_window_names()
#exit()

#create object
#insert 'none' into argument to capture whole screen. 15:00 vid 5
wincap = WindowCapture('Diablo II: Resurrected')
#Init Vision Class; because it not gonna change inside main loop:
Vision_zombie = Vision('zombie_1.jpg')
#Init trackbar Window
Vision_zombie.init_control_gui()


loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()

    #Pre-Processing of Image
    output_image = Vision_zombie.apply_hsv_filter(screenshot)

    #Do object detection
    #rectangles = Vision_zombie.find(screenshot, 0.40)

    #draw the dtection results onto the original image
    #output_image = Vision_zombie.draw_rectangles(screenshot,rectangles) #inserts image and list of rectangles. returns output
    
    #display the processed image
    cv.imshow('Matches', output_image)
    
    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #'pressing "Q" will exit
    #Waits 1ms every loop
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')