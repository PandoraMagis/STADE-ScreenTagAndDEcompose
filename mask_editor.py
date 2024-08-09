from tkinter import Canvas
from enum import Enum

    
class Mask :
    
    class Mode(Enum):
        """Mode types for the type of mask.
            Types are autonomics
        """
        Line = 1
        Square = 2
        Circle = 3
        
    def __init__(self, event, img_holder, ssr_object, mode : Mode) -> None:
        # initialasing the positions
        self.init_pos = event.x, event.y
        self.last_pos = event.x, event.y
        # canva and image object
        self.img_holder = img_holder
        self.canva :Canvas = self.img_holder.canva
        self.img = ssr_object
        # mode and mask saving object
        self.mode = mode
        self.mask = None        # ID of shape on the canvas
        self.mask_shape = []    # Mask position/shape on raw image
        
    def draw(self, event) : 
        # decompose element for facility
        last_x, last_y = self.last_pos
        
        if self.mode == Mask.Mode.Line : 
            self.last_pos = event.x, event.y
            new_x, new_y = self.last_pos
            #TODO - not realy viable - polygon must be better the end
            draw_pos = (last_x, last_y, new_x, new_y)
            self.mask_for_raw_img(draw_pos)
            self.draw_line(draw_pos)
        else:
            new_x, new_y = event.x, event.y
            self.canva.delete(self.mask)       
            if self.mode == Mask.Mode.Circle :
                # radius is a little bit boring to compute so i use this monstuosity
                radius_x = abs(last_x - new_x)
                radius_y = abs(last_y - new_y)
                draw_pos = (last_x-radius_x, last_y-radius_y, new_x+radius_x, new_y+radius_y)
                self.mask_for_raw_img(draw_pos)
                self.draw_circle(draw_pos)
            elif self.mode == Mask.Mode.Square :
                draw_pos = (last_x, last_y, new_x, new_y)
                self.mask_for_raw_img(draw_pos)
                self.draw_square(draw_pos)
        
    
    def draw_square(self, draw_pos) :
        self.mask = self.canva.create_rectangle(draw_pos, fill='blue')
    
    def draw_line(self, draw_pos) : 
        self.canva.create_line(draw_pos, fill='red')
    
    def draw_circle(self, draw_pos) : 
        self.mask = self.canva.create_oval(draw_pos, fill='purple')
        
    def resize(self, draw_pos, for_raw = True) : 
        # get size of canva
        w_x, w_y = self.img_holder.img_size
        # get size of raw image
        i_x, i_y = self.img.screenshot.size
        
        img_ratio_x = (i_x / w_x) if i_x > i_y else  (i_y / w_y)
        
        # adaptating mask size
        draw_pos = tuple( int(i*img_ratio_x) if for_raw else int(i/img_ratio_x) for i in draw_pos)
        return draw_pos
    
    def mask_for_img_holder(self) :
        if self.mode == Mask.Mode.Line :
            for draw_pos in self.mask_shape :
                new_pos = self.resize(draw_pos, for_raw=False)
                self.draw_line(new_pos)
        else :
            draw_pos = self.resize(self.mask_shape, for_raw=False)
            if self.mode == Mask.Mode.Circle :
                self.draw_circle(draw_pos)
            elif self.mode == Mask.Mode.Square :
                print(f"draw swaure on {draw_pos}, window shape = {self.img.screenshot.size}")
                self.draw_square(draw_pos)
            

    def mask_for_raw_img(self, draw_pos) :
        draw_pos = self.resize(draw_pos, for_raw=True)
        # saving the mask
        if self.mode == Mask.Mode.Line :
            self.mask_shape.append(draw_pos)
        else :
            self.mask_shape = draw_pos
            
    def save_mask(self) :
        # get mask for raw image size
        #TODO - will crsh for a line mask
        x_start, y_start, x_end, y_end = self.mask_shape
        mask_type = self.mode
        
        # get img info
        img_number = self.img.img_number
        img_path = self.img.img_name
        
        # final mask to write
        mask_str = [img_number, img_path ,mask_type ,x_start, y_start, x_end, y_end]
        mask_str = [ str(i) for i in mask_str]
        mask_str = ','.join(mask_str) + '\n'
        # open and append to the end of the file 
        with open('mask.csv', 'a') as file:
            file.write(mask_str)
        
        
    def __str__(self) -> str:
        #TODO - change this to be used in save mask BUT care for mask not fully initialised
        return f"Mask on image {self.img.img_name}, drawing with {self.mode} on {self.canva}, last pos {self.last_pos}"