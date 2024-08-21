import cv2 as cv
import numpy as np
import os
from time import time
from Window_Capture import WindowCapture
from vision import Vision
#from hsvwindow import HsvWindow

#WindowCapture.list_window_names()
#exit()

wincap = WindowCapture('Diablo II: Resurrected')
#Init Vision Class; because it not gonna change inside main loop:
Vision_zombie = Vision('zombie_1_processed.jpg')
# Init trackbar Window
#Vision_zombie.init_control_gui()

#Zombie HSV FIlter [ Just brighter screen]
#hsv_filter = HsvWindow(0,0,0,179,255,255,0,0,36,0)

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()

    #Pre-Processing of Image, 2nd argument applies filter values
    #processed_image = Vision_zombie.apply_hsv_filter(screenshot,hsv_filter) 

    #Do object detection
    rectangles = Vision_zombie.find(screenshot, 0.40) #change to "processed_image" if u want to apply filter

    #draw the dtection results onto the original image
    output_image = Vision_zombie.draw_rectangles(screenshot,rectangles) #inserts image and list of rectangles. returns output
    
    #display the processed image
    #cv.imshow('Processed Image', processed_image) #processed image window
    cv.imshow('Matches', output_image)
    
    
    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #'pressing "Q" will exit
    #Waits 1ms every loop
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')