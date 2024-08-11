import tkinter as tk
from random import randrange

class Tag :
    def __init__(self, host_frame, text, grid_place_obj, select_tag_signal = ()) -> None:
        # interface communication TODO find an otehr way 
        self.select_tag_signal = select_tag_signal if select_tag_signal is not None else ()
        self.host_fram = host_frame
        # create btn 1st so i can get the geometry
        self.btn_tag_frame = tk.Button(host_frame, text=text, font=('roboto',15), fg='black')
        # computing the grid pos in a way where it doesnt geos off the window
        self.grid_row, self.grid_col = self.grid_geom_compute(grid_place_obj)
        # giving it a random color that can change with click
        self.change_color()
        
        # right click = change color
        self.btn_tag_frame.bind('<Button-3>', self.change_color )
        # click = apply Tag 
        self.btn_tag_frame.bind('<Button-1>', self.tag_click_select )
        # double click = create/add tag shape
        self.btn_tag_frame.bind('<Double-Button-1>', self.tag_double_click )
        
        self.btn_tag_frame.grid(row= self.grid_row, column = self.grid_col , padx=1, pady=3)
        
    def tag_click_select(self, e) : 
        # pure genious or just despair once again i lead my self in new untold circular ref places
        self.select_tag_signal(self, False)
    
    def tag_double_click(self, e) : 
        self.select_tag_signal(self, True)
        
    
    def grid_geom_compute(self, dict_obj, add=True) : 
        # print(f"row {row} ; col  {col}")
        
        main_w = self.host_fram.winfo_width()
        main_h = self.host_fram.winfo_height()
        
        tag_w = self.btn_tag_frame.winfo_reqwidth()
        tag_h =  self.btn_tag_frame.winfo_reqheight()
        
        _, col = dict_obj.values()
        col += 1 # cause the first button isn't registered
        
        print(f" tagw{tag_w} * col{col} = {tag_w * col} > {main_w} : main w")
        if (tag_w+5) * col > main_w : 
            dict_obj["row"] += 1
            dict_obj["col"] = 0
        else :
            dict_obj["col"] +=1
       
        row, col = dict_obj.values()
        
        # self.btn_tag_frame.w
        print(f"geoms : {main_w}x{main_h} vs {tag_w}x{tag_h}")
        
        return row, col 
        
        
        
        
    
    def change_color(self, e = None) : 
        # some color sometimes crash, since i don't want to be a color picker perfectionist but just a pick me i will not care and laucnh in reccursive until it give one correct 
        try : 
            self.colors = [ randrange(0,255) for _ in range(3) ]
            color = ''.join([ str(hex(i)[-2:]).upper() for i in self.colors])
            self.btn_tag_frame.config(bg=f"#{color}") 
        except tk.TclError as e : 
            self.change_color()
        
    # shit + click = default
    
    