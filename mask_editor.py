from tkinter import Canvas

class Mask :
    
    def __init__(self, event, canva : Canvas, ssr_object) -> None:
        self.last_pos = event.x, event.y
        self.canva = canva
        self.img = ssr_object
        # self.mode = "rectangle"
        
    
    def draw(self, event) : 
        last_x, last_y = self.last_pos
        self.last_pos = event.x, event.y
        new_x, new_y = self.last_pos
        draw_pos = (last_x, last_y, new_x, new_y)
        self.draw_line(draw_pos)
        
    
    def draw_square(self) :
        self.canva.create_rectangle()
        pass
    
    def draw_line(self, draw_pos) : 
        self.canva.create_line(draw_pos, fill='red')
        
    def __str__(self) -> str:
        return f"Mask on image {self.img.img_name}, drawin on {self.canva}, last pos {self.last_pos}"