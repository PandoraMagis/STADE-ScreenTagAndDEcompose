from tkinter import Canvas
from enum import Enum

    
class Mask :
    class Mode(Enum):
        Line = 1
        Square = 2
        Circle = 3
        
    def __init__(self, event, canva : Canvas, ssr_object, mode : Mode) -> None:
        self.last_pos = event.x, event.y
        self.canva = canva
        self.img = ssr_object
        self.mode = mode
        self.mask = None
        
    def draw(self, event) : 
        last_x, last_y = self.last_pos
        
        if self.mode == Mask.Mode.Line : 
            self.last_pos = event.x, event.y
            new_x, new_y = self.last_pos
            #TODO - not realy viable - polygon must be better the end
            self.draw_line((last_x, last_y, new_x, new_y))
        else:
            new_x, new_y = event.x, event.y
            self.canva.delete(self.mask)       
            if self.mode == Mask.Mode.Circle :
                radius_x = abs(last_x - new_x)
                radius_y = abs(last_y - new_y)
                draw_pos = (last_x-radius_x, last_y-radius_y, new_x+radius_x, new_y+radius_y)
                self.draw_circle(draw_pos)
            elif self.mode == Mask.Mode.Square :
                draw_pos = (last_x, last_y, new_x, new_y)
                self.draw_square(draw_pos)
        
    
    def draw_square(self, draw_pos) :
        self.mask = self.canva.create_rectangle(draw_pos, fill='blue')
    
    def draw_line(self, draw_pos) : 
        self.canva.create_line(draw_pos, fill='red')
    
    def draw_circle(self, draw_pos) : 
        self.mask = self.canva.create_oval(draw_pos, fill='purple')
        
    def __str__(self) -> str:
        return f"Mask on image {self.img.img_name}, drawing with {self.mode} on {self.canva}, last pos {self.last_pos}"