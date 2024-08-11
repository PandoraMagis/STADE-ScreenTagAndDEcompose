import tkinter as tk
from random import randrange

class Tag :
    def __init__(self, host_frame, text) -> None:
        self.btn_tag_frame = tk.Button(host_frame, text=text, font=('roboto',15), fg='black')
        self.change_color()
        
        # right click = change color
        self.btn_tag_frame.bind('<Button-3>', self.change_color)
        # click = apply Tag
        self.btn_tag_frame.bind('<Button-1>', lambda e : print("click") )
        # double click = create/add tag shape
        
        # 
        self.btn_tag_frame.pack()
        
        pass
    

    
    def change_color(self, e = None) : 
        # some color sometimes crash, since i don't want to be a color picker perfectionist but just a pick me i will not care and laucnh in reccursive until it give one correct 
        try : 
            self.colors = [ randrange(0,255) for _ in range(3) ]
            color = ''.join([ str(hex(i)[-2:]).upper() for i in self.colors])
            self.btn_tag_frame.config(bg=f"#{color}") 
        except tk.TclError as e : 
            self.change_color()
        
    # shit + click = default
    
    