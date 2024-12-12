import cv2 as cv
import numpy as np
import os
import keyboard
from time import sleep, time
from Window_Capture import WindowCapture
from vision import Vision
import pyautogui
from threading import Thread
from pindle import pindle_script
from pindle import nihlathak_portal_search

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
#MP1 = Vision(None)
#HP1 = Vision(None)

#Potion Code ------------------------------------------------------
#HP1 = Vision('items/potions/1HP.jpg')
#MP1 = Vision('items/potions/1MP.jpg')
JV35 = Vision('items/potions/35JV.jpg')
nihl_portal = Vision('items/misc/NithalakPortal.jpg')

health_potions = [
    Vision('items/potions/1HP.jpg'),
    Vision('items/potions/2HP.jpg'),
    Vision('items/potions/3HP.jpg'),
    Vision('items/potions/4HP.jpg'),
    Vision('items/potions/5HP.jpg')
    
]
mana_potions = [
    Vision('items/potions/1MP.jpg'),
    Vision('items/potions/2MP.jpg'),
    Vision('items/potions/3MP.jpg'),
    Vision('items/potions/4MP.jpg'),
    Vision('items/potions/5MP.jpg')
]


is_bot_in_action = False         #Default Set to False. True if you dont want any BotAction

#detections "Interrupt service routine" [Inside of a Thread]
def bot_interrupt_detection(hpots,mpots):
    global is_bot_in_action
    if len(hpots_combined) > 0:
        bot_actions_HP(hpots_combined)
    elif len(mpots_combined) > 0:
        bot_actions_MP(mpots_combined)
    is_bot_in_action = False
    
#this function gets performed inside another thread: [must call this function]
# def bot_actions(hpots):
#     targets = HP1.get_click_points(hpots)
#     target = wincap.get_screen_position(targets[0])
#     pyautogui.moveTo(x=target[0], y=target[1])
#     sleep(0.1)
#     #pyautogui.click()
#     pyautogui.press('e')
#     print(target[0],target[1])
#     sleep(0.2)

#Health potion Bot Action:
def bot_actions_HP(hpots_combined):
    for hpot in hpots_combined:
        # Get the corresponding Vision object for each potion
        targets = health_potions[0].get_click_points([hpot])  # Assuming all mpots use the same Vision object
        if targets:  # Ensure there are targets found
            target = wincap.get_screen_position(targets[0])
            pyautogui.moveTo(x=target[0], y=target[1])
            #sleep(0.1)
            pyautogui.press('e')  # Simulate pressing 'e'
            print(f"HEALTH Potion clicked at: {target[0]}, {target[1]}")
            sleep(0.2)

def bot_actions_MP(mpots_combined):
    for mpot in mpots_combined:
        # Get the corresponding Vision object for each potion
        targets = mana_potions[0].get_click_points([mpot])  # Assuming all mpots use the same Vision object
        if targets:  # Ensure there are targets found
            target = wincap.get_screen_position(targets[0])
            pyautogui.moveTo(x=target[0], y=target[1])
            #sleep(0.1)
            pyautogui.press('e')  # Simulate pressing 'e'
            print(f"Mana Potion clicked at: {target[0]}, {target[1]}")
            sleep(0.2)

#PINDLE 
def on_press_f9():
    print("F9 Pressed!")
    pindle_script(wincap,screenshot,nihl_portal)
keyboard.add_hotkey('F9', on_press_f9)

loop_time = time()
health = 100

while(True):
    screenshot = wincap.get_screenshot()
    output_image = screenshot.copy()
    #object Detection, will look at screenshot and return list of rectangles where obj is found
    #rectangles = cascade_zombie.detectMultiScale(screenshot)
    #draw detection results onto original image:
    #detection_image = vision_zombie.draw_rectangles(screenshot, rectangles)

    #rectangles = minor_hp_pot.find(screenshot, 0.40)
    #hpots = HP1.find(screenshot,0.95)
    #output_image = HP1.draw_rectangles(screenshot,rectangles)

    #Pindle Script:

    if health <= 80:
        #health pots
        hpots_combined = []
        for hp_vision in health_potions:
            hpots = hp_vision.find(screenshot,0.97)
            hpots_combined.extend(hpots)
            output_image = hp_vision.draw_rectangles(output_image, hpots)

        #mana pots
        mpots_combined = []
        for mp_vision in mana_potions:
            mpots = mp_vision.find(screenshot,0.97)
            mpots_combined.extend(mpots)
            output_image = mp_vision.draw_rectangles(output_image, mpots)
    #tg = Vision_minor_mana_pot.get_click_points(mpots)
    cv.imshow('Matches', output_image)

    #display the processed image
        #cv.imshow('Processed Image', processed_image) #processed image window
    #cv.imshow('Matches', detection_image)

    # take bot actions
    if not is_bot_in_action:
        is_bot_in_action = True
        if health <= 80:
            t = Thread(target=bot_interrupt_detection, args=(hpots,mpots)) #needs to be sent as a tuple.
            t.start()
    #print('FPS {}'.format(1 / (time() - loop_time)))
    #print("# of Health Pots: " ,len(hpots_combined), "# of Mana Pots: ", len(mpots_combined))
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

    #Listen for 'F9' Press {PINDLE}

print('Done.')