import cv2 as cv
import numpy as np
import os
from time import sleep, time
from Window_Capture import WindowCapture
from vision import Vision
import pyautogui
from threading import Thread

#removable code:
pos_count = 0
neg_count = 0
#WindowCapture.list_window_names()
#exit()

wincap = WindowCapture('Diablo II: Resurrected')

#Loading trained model:
cascade_zombie = cv.CascadeClassifier('cascade_classifier/cascade/cascade.xml')
#loading empty Vision class
vision_zombie = Vision(None)

is_bot_in_action = False

#this function gets performed inside another thread: [must call this function]
# def bot_actions(rectangles):
#     #Bot actions:
#     if len(rectangles) > 0:
#         #grab first objects, and find the place to click
#         targets = vision_zombie.get_click_points(rectangles)
#         target = wincap.get_screen_position(targets[0])
#         pyautogui.click(x=target[0], y=target[1])   #moves mouse there
#         pyautogui.click()
#         print("moving mouse!")
#         sleep(1)
#     #leting main loop know when this thread is done/completed:
#     global is_bot_in_action
#     is_bot_in_action = False

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()

    #object Detection, will look at screenshot and return list of rectangles where obj is found
    rectangles = cascade_zombie.detectMultiScale(screenshot)
    #draw detection results onto original image:
    detection_image = vision_zombie.draw_rectangles(screenshot, rectangles)

    #display the processed image
    #cv.imshow('Processed Image', processed_image) #processed image window
    cv.imshow('Matches', detection_image)

    #take bot actions
    # if not is_bot_in_action:
    #     is_bot_in_action = True
    #     t = Thread(target=bot_actions, args=(rectangles,)) #needs to be sent as a tuple.
    #     t.start()
    
    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #'pressing "Q" will exit
    #Waits 1ms every loop
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    # elif key == ord('f'):
    #     cv.imwrite('cascade_classifier/positive/{}.jpg'.format(loop_time), screenshot)
    #     pos_count += 1
    #     print("saved Positive Image #", pos_count)
    # elif key == ord('d'):
    #     cv.imwrite('cascade_classifier/negative/{}.jpg'.format(loop_time), screenshot)
    #     neg_count += 1
    #     print("saved Negative Image #", neg_count)

print('Done.')