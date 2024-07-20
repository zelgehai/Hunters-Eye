import cv2 as cv
import numpy as np
import os
import pyautogui

while(True):
    screenshot = pyautogui.screenshot() #need to format this screenshot to opencv format
    screenshot = np.array(screenshot)
    #screenshot = screenshot[:, :, ::-1].copy() #converts RGB format 
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) #same as above code

    cv.imshow('Computer Vision', screenshot)

    #'pressing "Q" will exit
    #Waits 1ms every loop
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')