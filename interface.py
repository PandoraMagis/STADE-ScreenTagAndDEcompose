import tkinter as tk
from PIL import Image, ImageTk
from system_hotkey import SystemHotkey

import screenshotRaw as SSR
from mask_editor import Mask

class interface :
    
    def __init__(self) -> None:
        
        # image accumulator
        self.img_loaded = [{"name":"laoding_screen"}]
        
        # img place holder
        self.loading_screen_img_obj = Image.open("loading_screen.png")
        
        # create a windows for everything
        root = tk.Tk()
        root.title("STADE - ScreenTagAndDEcompose")
        root.minsize(480,360)
        # root.iconbitmap("logo.ico") # icon of window - todo
        root.config(background='#dcdcddddc')
        
        ### tag frame ###
        tag_frame = tk.Frame(root, bg = '#000')
        btn_new_tag = interface.btn(tag_frame, "new tag")
        btn_new_tag.pack()
        tag_frame.pack(fill=tk.X, anchor='n')
        
        ### working frame ### -- place of the screen shot and mask edit
        work_frame = tk.Frame(root, bg='#FF00FF')
        work_frame.pack(expand='yes', fill=tk.BOTH)
        
        ### tests ### -- at the top menu place - example but maybe used
        test_btn = interface.btn(root)
        test_btn.pack()
        # txt crea - just an example for now
        # labelx = Label(PLACE, text="...", font=('roboto', 15), bg='', fg='white')
        # labelx.pack(placeargs)
        
        ### image holder ### -- hold the screen shot inside workframe
        img_holder = interface.img(work_frame)       
        img_holder.canva.pack(expand=1, fill=tk.BOTH)
        img_holder.load_img(self.loading_screen_img_obj)
        self.img_index = 0
        

        
        # frame class attribution
        self.work_frame = work_frame
        self.img_holder = img_holder
        self.tag_frame = tag_frame
        self.tag_btns = [btn_new_tag]

        #TODO tag box - shift click a tag make it auto for next screen shot
        #TODO menu - config
        #TODO top bar for scheme
        #TODO bottom if height enough - chosse img
        #TODO action molette scroll to zoom - in/out on the screen (user precision to place mask)
        
        ##########  Actions
        # --- RESIZE ---  action on resire window - resize all the elements
        root.bind('<Configure>', self.resize_window)
        
        # --- ScreenShot --- action to take a screenshot and change img loaded - bind hotkey to look even out of program
        hk = SystemHotkey() # -- if smth goes wrong do this [[collections.Iterable = collections.abc.Iterable]] - in the lib
        hk.register(['kp_0'], callback = lambda e : self.screen_taken(e)) # keys possible : https://github.com/timeyyy/system_hotkey/blob/master/system_hotkey/system_hotkey.py and https://github.com/timeyyy/system_hotkey/blob/master/system_hotkey/keysymdef.py
        
        # --- MASK Actions --- on mouse click draw thing on working frame/canva
        self.active_masks = []
        img_holder.canva.bind('<Button-1>', lambda e : self.start_mask(e, Mask.Mode.Square))
        img_holder.canva.bind('<Control-1>', lambda e : self.start_mask(e, Mask.Mode.Circle))
        img_holder.canva.bind('<Shift-1>', lambda e : self.start_mask(e, Mask.Mode.Line))
        # the mask update while dragging mouse
        img_holder.canva.bind('<B1-Motion>', self.continue_mask)
        # the mask close and save when it's all done
        img_holder.canva.bind('<B1-ButtonRelease>', self.stop_mask)
        # ctrl-z delete last mask
        
        # --- Button Actions --- 
        # create new tag action
        btn_new_tag.bind('<Button-1>', lambda e: print("clicked"))
        
        root.mainloop()
        
    def resize_window(self, event) : 
        # on resizing root actions
        self.img_holder.resize_img(event)
        #TODO - resize and reprint the masks
        for mask in self.active_masks :
            mask.mask_for_img_holder()

    def screen_taken(self,event) : 
        new_screen = SSR.ScreeenRaw(saving_path="Images/", subjetc="test_dev")
        self.img_holder.load_img(new_screen.take())
        self.img_loaded.append( new_screen )
        self.img_index = self.img_loaded.index(new_screen)
    
    # Mask
    def start_mask(self, event, mask_mode) :
        working_img = self.img_loaded[self.img_index]
        if isinstance(working_img, dict) : return # dont launch if we are on the loading_screen
        self.current_mask = Mask(event, self.img_holder, self.img_loaded[self.img_index], mask_mode)
    
    def continue_mask(self, event) :
        working_img = self.img_loaded[self.img_index]
        if isinstance(working_img, dict) : return # dont launch if we are on the loading_screen
        if self.current_mask is None : raise RuntimeError("Continuing mask imppossible, no image mask are currently open")
        self.current_mask.draw(event)
        
    def stop_mask(self, event) :
        print(f"finish {self.current_mask}")
        self.active_masks.append(self.current_mask)
        #TODO disk save the mask
        self.current_mask.save_mask()
        
        
        
    # class menu :
    
    
    # class tag_bar :
        
    # class tuto : 
    
    class img : 
        def __init__(self, frame) :
            self.host_frame = frame
            self.canva = tk.Canvas(frame)
            # self.laod = 15
            
        def info_pixel(self):
            # updtae needed before geting infos of hight - dont work before pack
            self.canva.update()
            winfo = (self.host_frame.winfo_width(), self.host_frame.winfo_height() )
            return winfo

        def load_img(self, img_object) :
            self.img_obj_raw = img_object
            # resize then print the img
            self.resize_img()
        
        def get_new_size_img(self, widht=None, height=None) :
            # fools keeper - maybe useless
            # if widht is None and height is None : raise ValueError("img resize asked without widht nor height")
            if widht is not None and height is not None : raise NotImplemented("img resize asked with widht AND height - idk what happend from this")
            if self.img_obj_raw is None : raise ValueError("img not loaded in container, new size can't be computed")
            
            # img infos for computing ratio and use it
            original_width, original_height = self.img_obj_raw.size
            img_aspect_ratio = original_width / original_height
            
            # window size and possible img resolution out come
            w_width, w_height  = self.info_pixel()
            img_new_width = int(w_height * img_aspect_ratio)
            img_new_height = int(w_width / img_aspect_ratio)
                        
            # compute final img size
            resize_width =  w_width  if w_width < img_new_width   else img_new_width
            resize_height = w_height if w_height < img_new_height else img_new_height
            
            resize_width, resize_height = (w_width, img_new_height) if w_width < img_new_width else (img_new_width, w_height)
            
            # print(f"image width info raw : {original_width} ; new : {img_new_width} ; window : {w_width} ; chosen : {resize_width}")
            # print(f"image height info raw : {original_height} ; new : {img_new_height} ; window : {w_height} ; chosen : {resize_height}")
            # if self.laod ==0 : exit()
            # self.laod -= 1
            self.img_size = (resize_width, resize_height)
            return self.img_size

        def resize_img(self, event=None):
            if self.img_obj_raw is None : raise ValueError("img not loaded in container, new size can't be computed")
            else : img_object = self.img_obj_raw
            
            resized_image = img_object.resize(self.get_new_size_img(img_object))
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canva.delete('all')
            self.canva.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            # self.canva.config(image=tk_image)
            # self.canva.image = tk_image  # Keep a reference to avoid garbage collection
            
    
    class btn :
        def __new__(self, frame, txt='no text btn') -> None:
            return tk.Button(frame, text=txt, font=('roboto',15), bg='white', fg='black')


if __name__ == "__main__" : 
    MyIntf = interface()