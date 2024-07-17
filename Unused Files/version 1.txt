import cv2 as cv
import numpy as np
#pyautogui -> automates keyboard + mouse movements [also allows locateonScreen]

#loading image format

default_image = cv.imread('img_1.jpg', cv.IMREAD_REDUCED_COLOR_2) #IMREAD_UNCHANGED
needle_image = cv.imread('zombie_1.jpg', cv.IMREAD_REDUCED_COLOR_2)

#calls matchtemplate
result = cv.matchTemplate(default_image, needle_image, cv.TM_CCOEFF_NORMED)

#cv.imshow('Result', result) #shows us the result in image format. Runs and closes instantly
#cv.waitKey()

#Get best pixel location [best match position]
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result) 

print('Best match top left position: %s' %str(max_loc))
print('Best match confidence: %s' % max_val)

#Threshold, because algorithm will always return a value; but not right img.
threshold = 0.8
if max_val >= threshold:
    print("found needle!")
    
    #dimensions of needle image
    needle_w = needle_image.shape[1]
    needle_h = needle_image.shape[0]

    #definitions:
    top_left = max_loc
    
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h) #using width + height of image
    #draw rectangle
    cv.rectangle(default_image, top_left, bottom_right,
                 color=(0, 255, 0), thickness=3, lineType=cv.LINE_4)
    
    cv.imshow('Result', default_image)
    cv.waitKey()
    #if you want to save result to file:
    #cv.imwrite('result.jpg', default_image)
else:
    print("Needle not found :(")