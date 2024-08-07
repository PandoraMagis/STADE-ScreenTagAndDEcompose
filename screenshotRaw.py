import pyautogui
import os, os.path
from datetime import datetime

class ScreeenRaw() :
    def __init__(self, saving_path, subjetc=None) -> None:
        if not os.path.isdir(saving_path) : raise ValueError("Saving path for screenshot isn't a valiable directory")
        self.saving_path = saving_path
        self.subject = subjetc
    
    def take(self) : 
        self.time = datetime.now()
        self.screenshot = pyautogui.screenshot(allScreens=True)
        self.save_screen()
        return self.screenshot
        
    
    def save_screen(self) :
        self.screenshot.save(self.create_name())
    
    def create_name(self) :
        # {nb img on folder + 1}_{date_hours_min_sec}.png
        # scoop nb file
        self.img_number = len([name for name in os.listdir(self.saving_path)])
        formated_date = self.time.strftime('%Y_%m_%d__%H_%M_%S')
        self.img_name = f"{self.saving_path}{self.img_number}___{self.subject+'___' if self.subject is not None else ''}{formated_date}.png"
        return self.img_name
        
        
if __name__ == "__main__" : 
    DIR = "Images/"
    print([name for name in os.listdir(DIR)])
    print(len([name for name in os.listdir(DIR)]))
    