import cv2 as cv
import numpy as np

def findClickPositions(needle_image_path, default_image, threshold = 0.6, debug_mode=None):

    #default_image = cv.imread(default_image_path, cv.IMREAD_REDUCED_COLOR_2) #IMREAD_UNCHANGED
    needle_image = cv.imread(needle_image_path, cv.IMREAD_REDUCED_COLOR_2)
    needle_w = needle_image.shape[1]
    needle_h = needle_image.shape[0]

    #calls matchtemplate
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(default_image, needle_image, method) #TM_SQDIFF_NORMED
    #returns confidence score
    #print(result)

   
    locations = np.where(result >= threshold)
    #np.where looks like this:
    #(array([334, 335]), array([91, 91]))
    #print(locations)

    #zip those into position tuples
    locations = list(zip(*locations[::-1]))
    #print(locations)

    #bulding list
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h] #build rectangle for each location
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5) #Grouping all rectangles that are close to eachother
    print(rectangles)

    points = []
    #printing box
    if len(rectangles):
        print('Found Needle.')

        needle_w = needle_image.shape[1]
        needle_h = needle_image.shape[0]
        line_color = (0,255,0)
        line_type = cv.LINE_4
        marker_color = (255,0,255)
        marker_type = cv.MARKER_CROSS

        #need to loop over all locations and draw their rectangle
        for (x,y,w,h) in rectangles:
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            #save the points
            points.append((center_x,center_y))

            if debug_mode == 'rectangles':
                #determine box positions:
                top_left = (x,y)
                bottom_right = (x+w, y+h)
                #Draw box
                default_image = default_image.copy() #Make a writable copy
                cv.rectangle(default_image, top_left, bottom_right, line_color, line_type)
            elif debug_mode == 'points':
                cv.drawMarker(default_image, (center_x,center_y), marker_color, marker_type)
            elif debug_mode == 'both':
                top_left = (x,y)
                bottom_right = (x+w, y+h)
                #Draw box
                cv.rectangle(default_image, top_left, bottom_right, line_color, line_type)
                #Draw Marker
                cv.drawMarker(default_image, (center_x,center_y), marker_color, marker_type)
        
    if debug_mode:    
        cv.imshow('Matches', default_image)    
        #cv.waitKey()
        #cv.imwrite('result.jpg', default_image)        
    
    return points
