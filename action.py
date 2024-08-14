import win32gui
import win32api
import win32con

from enum import Enum
import ctypes

class Action :
    
    class Dofus_Action(Enum):
        """Mode types for the type of mask.
            Types are autonomics
        """
        BASE_LINE = (1920,1080)
        Go_RIGHT = (1570,600)
        Go_LEFT = (100,200)
        Go_UP = (1200,10)
        Go_DOWN = (1200,900)
        DIALOGUE_NEXT = 3
        JOIN_GRP_FIGHT = 3
        
    def __init__(self, window_name, baseline) -> None:
        self.hwnd = win32gui.FindWindow(None, window_name)
        self.baseline = baseline
    
    def click_self(self, action = None) :
        x, y = self.action_pos if action is None else action.value
        Action.click(x, y, self.hwnd, self.baseline)
    
    def click(x, y, hwnd, baseline):
        # window info retrive
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        
        left, right = (-1 * left, -1 * right) if left < 0 else (left, right)
        top, bottom = (-1 * top, -1 * bottom) if top < 0 else (top, bottom)
        
        print(f"pos: {left}x{top} to {right}x{bottom} -- try to go @ {x}x{y}")

        width, height = left - right , top - bottom
        # width, height = left - right , top - bottom
        
        x_final = left + x
        y_final = top + y
        print(f"1st  : window size : {width}x{height} pos: {left}x{top} to {right}x{bottom} -- cursor ar {x_final}x{y_final} -- try to go @ {x}x{y}")
        
        width_base, height_base = baseline.value
        x_ratio, y_ratio = width_base / width ,     height_base / height
        x_final, y_final = int( x / x_ratio ) ,     int( y / y_ratio )
        
        print(f"2nd  : window size : {width}x{height} ref: {width_base}x{height_base}             -- cursor ar {x_final}x{y_final} -- try to go @ {x}x{y}")
        
        lParam = win32api.MAKELONG(x_final, y_final)
        
        
        # hWnd1= win32gui.FindWindowEx(hWnd, None, None, None)
        # win32api.SetCursorPos((x_final, y_final)) #for dev
        # win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        # win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
        
    def correct_size(windo_shape, ref_shape, ref_x, ref_y) :
        w_x, w_y = windo_shape
        # get size of raw image
        i_x, i_y = ref_shape
        
        img_ratio_x = i_x / w_x
        img_ratio_y = i_y / w_y
        
        # adaptating mask size
        pos = tuple( int(img_ratio_x * ref_x), int(img_ratio_y * ref_y) )
        return pos
    

if "__main__" == __name__ :
    # Action.click(1200,100) # gogogadegeto test
    
    # working on 4k split resolution
    # Action.click(1600,800) # go right
    # Action.click(100,200) # go left
    # Action.click(1200,900) # go bottom
    # Action.click(800,7) # go up
    
    monitors = win32api.EnumDisplayMonitors()
    primary_monitor_info = win32api.GetMonitorInfo(monitors[0][0])
    primary_monitor_rect = primary_monitor_info['Monitor']
    print(monitors)
    
    window_name = "Vamy - Dofus 2.72.0.9"
    
    my_action = Action(window_name, Action.Dofus_Action.BASE_LINE)
    
    # my_action.click_self(Action.Dofus_Action.Go_UP)
    # my_action.click_self(Action.Dofus_Action.Go_DOWN)
    # my_action.click_self(Action.Dofus_Action.Go_LEFT)
    my_action.click_self(Action.Dofus_Action.Go_RIGHT)