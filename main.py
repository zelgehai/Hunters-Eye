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
HP1 = Vision(None)

#Potion Code ------------------------------------------------------
HP1 = Vision('items/potions/1HP.jpg')
MP1 = Vision('items/potions/1MP.jpg')
JV35 = Vision('items/potions/35JV.jpg') 


is_bot_in_action = False         #Default Set to False. True if you dont want any BotAction

#detections "Interrupt service routine" [Inside of a Thread]
def bot_interrupt_detection(hpots,mpots):
    global is_bot_in_action
    if len(hpots) > 0:
        bot_actions(hpots)
    elif len(mpots) > 0:
        bot_actions_MP(mpots)
    is_bot_in_action = False
    
#this function gets performed inside another thread: [must call this function]
def bot_actions(hpots):
    targets = HP1.get_click_points(hpots)
    target = wincap.get_screen_position(targets[0])
    pyautogui.moveTo(x=target[0], y=target[1])
    sleep(0.1)
    #pyautogui.click()
    pyautogui.press('e')
    print(target[0],target[1])
    sleep(0.2)

def bot_actions_MP(mpots):
    targets = MP1.get_click_points(mpots)
    target = wincap.get_screen_position(targets[0])
    pyautogui.moveTo(x=target[0], y=target[1])
    sleep(0.1)
    pyautogui.press('e')
    print(target[0],target[1])
    sleep(0.2)

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()

    #object Detection, will look at screenshot and return list of rectangles where obj is found
    #rectangles = cascade_zombie.detectMultiScale(screenshot)
    #draw detection results onto original image:
    #detection_image = vision_zombie.draw_rectangles(screenshot, rectangles)

    #rectangles = minor_hp_pot.find(screenshot, 0.40)
    hpots = HP1.find(screenshot,0.95)
    #output_image = HP1.draw_rectangles(screenshot,rectangles)

    #mana
    mpots = MP1.find(screenshot,0.99)
    #tg = Vision_minor_mana_pot.get_click_points(mpots)
    output_image = MP1.draw_rectangles(screenshot,mpots) # can replace mpots with tg
    cv.imshow('Matches', output_image)

    #display the processed image
        #cv.imshow('Processed Image', processed_image) #processed image window
    #cv.imshow('Matches', detection_image)

    # take bot actions
    if not is_bot_in_action:
        is_bot_in_action = True
        t = Thread(target=bot_interrupt_detection, args=(hpots,mpots)) #needs to be sent as a tuple.
        t.start()
    #print('FPS {}'.format(1 / (time() - loop_time)))
    #print("# of Health Pots: " ,len(rectangles), "# of Mana Pots: ", len(mpots))
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