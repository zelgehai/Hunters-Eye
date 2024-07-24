import numpy as np
import win32gui, win32ui, win32con
from ctypes import windll

class WindowCapture:
    #Monitor width and height
    w = 0 # set this
    h = 0 # set this
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x =0
    offset_y =0

    #constructor
    def __init__(self, window_name) -> None:

        self.hwnd = win32gui.FindWindow(None, window_name)
        #Refer to Video #5, 3:00 if problems occur.
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))
        
        #Get window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]    #x coordinate 
        self.h = window_rect[3] - window_rect[1]    #y

        #account for window border
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels- border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        #set the cropped coordinates offset so we can translate screenshot
        #images into actual screen positions [might be wrong here]
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        windll.user32.SetProcessDPIAware()
        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, self.w, self.h)
        save_dc.SelectObject(bitmap)
        #save_dc.BitBlt((0,0),(self.w,self.h) , mfc_dc, (self.cropped_x,self.cropped_y) , win32con.SRCCOPY)

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)

        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = np.ascontiguousarray(img)[..., :-1]  # make image C_CONTIGUOUS and drop alpha channel

        if not result:  # result should be 1
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwnd_dc)
            raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")
        #img = img[self.cropped_y:self.h, self.cropped_x:self.w]
        return img
        #This code Would give me a black screenshot with D2R
        #Updated with above code.
        '''
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x,self.cropped_y), win32con.SRCCOPY)
        #save screenshot
        #dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
        SignedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(SignedIntsArray, dtype='uint8')
        img.shape = (self.h,self.w,4)
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        #Drop the Alpha channel on the image [all of the transparency]
        #will cause problems with MatchTemplate if we don't
        img = img[...,:3] #Slow Code Can be Improved.
        #Draw_rectangles caused errors. TypeError: an integer is required (got type tuple)
        img = np.ascontiguousarray(img)
        return img
        '''
    
        #Get List of Windows
    @staticmethod   #Decorator Above the Method, and deleted self parameter.
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler,None)

    #only gonna work if you dont move around your game window.
    def get_screen_position(self,pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)