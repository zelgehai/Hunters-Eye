#Pindle Script
from time import sleep
import pyautogui


def pindle_script(wincap,screenshot,nihl_portal):
    print("Pindle has been triggered!")
    #moving down from Waypoint
    pos = wincap.get_screen_position((320,561))
    pyautogui.moveTo(pos[0],pos[1]) 
    pyautogui.click()
    sleep(1)

    pos = wincap.get_screen_position((640,600))
    pyautogui.moveTo(pos[0],pos[1]) 
    pyautogui.click()
    sleep(1)

    pos = wincap.get_screen_position((320,561))
    pyautogui.moveTo(pos[0],pos[1]) 
    pyautogui.click()
    sleep(1)

    screenshot = wincap.get_screenshot()
    print("looking for Nihlathak Temple")
    sleep(2)
    nihlathak_portal_search(wincap,screenshot,nihl_portal)

    # window_position = wincap.get_screen_position((320,561))
    # x,y = pyautogui.position()
    # print("x=",x, "y=",y)
    # print("Moving to ",window_position[0],window_position[1]," game window:")
    # pyautogui.moveTo(window_position[0], window_position[1]) #x,y cordinates
    print("done")
    print("------------------")

def nihlathak_portal_search(wincap, screenshot, nihl_portal):
    print("function nihl works")

    # Search for the Nihlathak portal in the screenshot
    nportal = nihl_portal.find(screenshot, 0.50)
    output_image = screenshot.copy()  # Copy screenshot to draw rectangles on

    # Draw rectangles around the found portal(s)
    output_image = nihl_portal.draw_rectangles(output_image, nportal)

    # Get the click points and click on the portal
    targets = nihl_portal.get_click_points(nportal)
    if targets:
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x=target[0], y=target[1])
        sleep(0.1)
        pyautogui.click()
        print("Found Portal! Clicked Portal")
        sleep(2)
    else:
        print("Nihlathak Portal not found.")