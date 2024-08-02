import cv2 as cv
import numpy as np
from hsvwindow import HsvWindow

class Vision:
    #Constants
    TRACKBAR_WINDOW = "Trackbars"
    #properties 
    needle_image = None
    needle_w = 0
    needle_h = 0
    method  = None

    def __init__(self, needle_image_path, method=cv.TM_CCOEFF_NORMED):
        #lead image trying to match
        self.needle_image = cv.imread(needle_image_path, cv.IMREAD_UNCHANGED)
        self.needle_w = self.needle_image.shape[1]
        self.needle_h = self.needle_image.shape[0]
        self.method = method

    def find(self, default_image, threshold = 0.6, max_results=10):

        #default_image = cv.imread(default_image_path, cv.IMREAD_REDUCED_COLOR_2) #IMREAD_UNCHANGED
        #needle_image = cv.imread(needle_image_path, cv.IMREAD_REDUCED_COLOR_2)
        #needle_w = needle_image.shape[1]
        #needle_h = needle_image.shape[0]

        #calls matchtemplate
        result = cv.matchTemplate(default_image, self.needle_image, self.method) #TM_SQDIFF_NORMED
        #returns confidence score
        #print(result)

    
        locations = np.where(result >= threshold)
        #np.where looks like this:
        #(array([334, 335]), array([91, 91]))
        #print(locations)

        #zip those into position tuples
        locations = list(zip(*locations[::-1]))
        #print(locations)

        #if no results, return now. This allows us to cocat together results, less errors
        if not locations:
            return np.array([], dtype=np.int32).reshape(0,4)
        
        #bulding list
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h] #build rectangle for each location
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5) #Grouping all rectangles that are close to eachother
        #print(rectangles)
        if len(rectangles) > max_results:
            print("Too many Results (Identified needles), raise the threshhold.")
            rectangles = rectangles[:max_results] #trancades results if > threhshold

        return rectangles

    def get_click_points(self,rectangles):
        points = []
        #printing box
        #if len(rectangles):
            #print('Found Needle.')
        '''
            line_color = (0,255,0)
            line_type = cv.LINE_4
            marker_color = (255,0,255)
            marker_type = cv.MARKER_CROSS
        '''
            #need to loop over all locations and draw their rectangle
        for (x,y,w,h) in rectangles:
            #Determines center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            #save the points
            points.append((center_x,center_y))
        return points

    #given list of [x,y,w,h] rectangles and canvas image to draw on, returns an image with the rectangles drawn.
    def draw_rectangles(self, default_image, rectangles):
        line_color = (0,255,0)
        line_type = cv.LINE_4

        for(x,y,w,h) in rectangles:
            #determines box positions:
            top_left = (x,y)
            bottom_right = (x+w, y+h)
            #draw the box
            default_image = default_image.copy() #Make a writable copy [working line of code]
            cv.rectangle(default_image, top_left, bottom_right, line_color, lineType=line_type)
        
        return default_image
    
    def draw_crosshairs(self, default_image, points):
        #BGR Colors
        marker_color = (255,0,255)
        marker_type = cv.MARKER_CROSS

        for(center_x, center_y) in points:
            #draw center point
            default_image = default_image.copy() #Make a writable copy [Not sure if this line works]
            cv.drawMarker(default_image, (center_x,center_y), marker_color, marker_type)
        return default_image

    '''
                if debug_mode == 'rectangles':
                    #determine box positions:
                    top_left = (x,y)
                    bottom_right = (x+w, y+h)
                    #Draw box
                    default_image = default_image.copy() #Make a writable copy [working line of code]
                    cv.rectangle(default_image, top_left, bottom_right, line_color, line_type)
                elif debug_mode == 'points':
                    default_image = default_image.copy() #Make a writable copy [Not sure if this line works]
                    cv.drawMarker(default_image, (center_x,center_y), marker_color, marker_type)
                elif debug_mode == 'both':
                    top_left = (x,y)
                    bottom_right = (x+w, y+h)
                    default_image = default_image.copy() #Make a writable copy [Not sure if this line works]
                    #Draw box
                    cv.rectangle(default_image, top_left, bottom_right, line_color, line_type)
                    #Draw Marker
                    cv.drawMarker(default_image, (center_x,center_y), marker_color, marker_type)
            
        if debug_mode:    
            cv.imshow('Matches', default_image)    
            #cv.waitKey()
            #cv.imwrite('result.jpg', default_image)        
        
        return points
    '''

    #Gui window with controls, for adjusting image arguments in real-time
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass

        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

    # returns an HSV filter object based on the control GUI values
    def get_hsv_filter_from_controls(self):
        # Get current positions of all trackbars
        hsv_filter = HsvWindow()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        return hsv_filter

    # given an image and an HSV filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV) #converts to HSV format

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv.split(hsv) #Splitting hsv into its components.
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v]) #Merged back

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])   #Minimum hue,saturation, and value
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)    #applying mask to original image

        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    # apply adjustments to an HSV channel
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    #Don't want certain values going over limit. For example, Saturation surpassing 255.
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c