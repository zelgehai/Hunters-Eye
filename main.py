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
MP1 = Vision(None)

#Potion Code ------------------------------------------------------
HP1 = Vision('items/potions/1HP.jpg')
MP1 = Vision('items/potions/1MP.jpg')
JV35 = Vision('items/potions/35JV.jpg') 


is_bot_in_action = False

#this function gets performed inside another thread: [must call this function]
def bot_actions(rectangles):
    #Bot actions:
    if len(rectangles) > 0:
        #grab first objects, and find the place to click
        targets = vision_zombie.get_click_points(rectangles)
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x=target[0], y=target[1])
        sleep(0.1)
        pyautogui.click()
        print("AMt of Rectangles:" , len(rectangles))
        print(target[0],target[1])
        print("moving mouse!")
        sleep(0.5)
    #leting main loop know when this thread is done/completed:
    global is_bot_in_action
    is_bot_in_action = False

def bot_actions_MP(mpots):
    #Bot actions:
    if len(mpots) > 0:
        #grab first objects, and find the place to click
        targets = MP1.get_click_points(mpots)
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x=target[0], y=target[1])
        sleep(0.1)
        #pyautogui.click(x=target[0], y=target[1])   #moves mouse there
        pyautogui.click()
        print("AMt of Mpots:" , len(mpots))
        print(target[0],target[1])
        print("moving mouse!")
        sleep(0.5)
    #leting main loop know when this thread is done/completed:
    global is_bot_in_action
    is_bot_in_action = False

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()

    #object Detection, will look at screenshot and return list of rectangles where obj is found
    #rectangles = cascade_zombie.detectMultiScale(screenshot)
    #draw detection results onto original image:
    #detection_image = vision_zombie.draw_rectangles(screenshot, rectangles)

    #rectangles = minor_hp_pot.find(screenshot, 0.40)
    rectangles = HP1.find(screenshot,0.95)
    #output_image = HP1.draw_rectangles(screenshot,rectangles)

    #mana
    mpots = MP1.find(screenshot,0.90)
    #tg = Vision_minor_mana_pot.get_click_points(mpots)
    output_image = MP1.draw_rectangles(screenshot,mpots) # can replace mpots with tg
    cv.imshow('Matches', output_image)

    #display the processed image
        #cv.imshow('Processed Image', processed_image) #processed image window
    #cv.imshow('Matches', detection_image)

    # take bot actions
    if not is_bot_in_action:
        is_bot_in_action = True
        t = Thread(target=bot_actions, args=(rectangles,)) #needs to be sent as a tuple.
        t.start()
    #pick up mana potions
    if not is_bot_in_action:
        is_bot_in_action = True
        t = Thread(target=bot_actions_MP, args=(mpots,)) #needs to be sent as a tuple.
        t.start()
    #print('FPS {}'.format(1 / (time() - loop_time)))
    print("# of Health Pots: " ,len(rectangles), "# of Mana Pots: ", len(mpots))
    
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