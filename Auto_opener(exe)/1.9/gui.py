# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from psutil import process_iter
import os

from commands import button_commands_logic

class Constructor_gui(Frame):
    text_field, info_button, info_programm = [], {}, {}
    
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        
        self.shortcuts_path = f'{os.getcwd()}\\shortcuts'
        self.save_path = f'{os.getcwd()}\\save\\save_path.txt' 
        self.save_open = f'{os.getcwd()}\\save\\save_open.txt' 
        
        self.add_img = ImageTk.PhotoImage(file=f"{os.getcwd()}\\image\\add.png")
        self.clear_img = ImageTk.PhotoImage(file=f"{os.getcwd()}\\image\\clear.png")
        self.save_img = ImageTk.PhotoImage(file=f"{os.getcwd()}\\image\\save.png")
        self.open_img = ImageTk.PhotoImage(file=f"{os.getcwd()}\\image\\open.png")
        self.close_img = ImageTk.PhotoImage(file=f"{os.getcwd()}\\image\\close.png")
    
    def windows_constructor(self, title, geometry, resizable, bg):
        self.master.attributes("-topmost",True) 
        self.master.title(title)
        self.master.geometry(f'{geometry[0]}x{geometry[1]}+{geometry[2]}+{geometry[3]}')
        self.master.resizable(resizable[0], resizable[1])
        self.master["bg"] = bg

        return self.master  
    
    def widgets_constructor(self, TYPE, BG, FG, FONT="Arial 10 bold"):
        widget = TYPE(self.master, bg = BG, fg = FG, font = FONT) 
    
        if TYPE != Button:
            self.text_field.append(widget)
    
        widget.pack_propagate(False)
        widget.pack(expand = True, fill = BOTH)
        return widget         
    
    def widgets_creating(self, commands):
        #---------------------------------------------------------------------
        widget = self.widgets_constructor(Listbox, "gray8", "white", "Arial 10")
        widget.place(x = 2, y = 46, height = 224, width = 388)       
        self.starter_content(widget, commands)
        #---------------------------------------------------------------------
        widget = self.widgets_constructor(Text, "gray8", "white", "Arial 11")
        widget.place(x = 30, y = 272, height = 27, width = 360)   
        #---------------------------------------------------------------------
        widget = self.widgets_constructor(Button, "gray30", "white")        
        widget.config(image = self.save_img, command=lambda: self.save_content())
        widget.place(x = 2, y = 3, height = 40, width = 40)
        #---------------------------------------------------------------------
        #VoxReguar
        widget = self.widgets_constructor(Button, "gray30", "white")
        widget.config(image = self.open_img, command=lambda: commands.Open())
        widget.place(x = 44, y = 3, height = 40, width = 172)
        #--------------------------------------------------------------------- 
        widget = self.widgets_constructor(Button, "gray30", "white")
        widget.config(image = self.close_img, command = lambda: commands.Close())
        widget.place(x = 218, y = 3, height = 40, width = 172)        
        #---------------------------------------------------------------------
        widget = self.widgets_constructor(Button, "gray30", "white")   
        widget.config(image = self.add_img, command = lambda: commands.adding_elem())
        widget.place(x = 2, y = 272, height = 26, width = 26)     
        #---------------------------------------------------------------------  
        
    def process_status(self, process_name):
        return len([proc.info['name']for proc in process_iter(['name'])\
                    if proc.info['name'] == process_name])    
    
    def save_content(self, exit=False):
        number_buttons, content = 0, ''
        for num in range(len(self.text_field[0].get(0,END))):
            if os.path.isfile(self.text_field[0].get(num)) == False:
                number_buttons += 1
                content += f'{self.text_field[0].get(num)}\n' 

        with open(self.save_open,'w') as file_open, open(self.save_path,'w') as file_path:
            file_path.write(f'buttons_len: {number_buttons}\n{content}')   
            file_open.seek(0)
            file_open.writelines([f'{self.info_programm[elem][1]}>>>{elem}\n'\
                                  for elem in self.info_programm\
                                  if len(self.info_programm[elem])-1 == 1])        
                  
        self.text_field.clear()
        self.info_button.clear()
        self.info_programm.clear()
        
        x, y = self.master.winfo_x(), self.master.winfo_y()
        self.master.destroy()
        if exit == False:
            run_gui(x,y)    
            
    def starter_content(self, widget, commands):
        with open(self.save_path,"r") as file_path, open(self.save_open,"r") as file_open,\
             os.scandir(self.shortcuts_path) as direct:
            try:
                number_buttons = int(file_path.readlines()[0][13:])
                file_path.seek(0)
                content = file_path.readlines()[1:]    
            except IndexError:
                content, number_buttons = [], 0
            
            for file in direct:
                if f'{file.name}\n' not in content:
                    number_buttons += 1
                    content.append(f'{file.name}\n') 
                self.info_programm[file.name] = [f'{self.shortcuts_path}\\{file.name}']
                
            if os.stat(self.save_open).st_size > 0:
                for line in file_open:
                    process_name = line.rstrip('\n')[0:line.find('>')]
                    key = line.rstrip('\n')[line.find('>')+3:]
                    
                    if self.process_status(process_name) > 0:
                        self.info_programm[key].append(process_name) 
                    else:
                        with open(self.save_open, "w"):
                            pass
                                  
        {(widget.insert(index, elem.rstrip('\n')),\
          commands.adding_elem(False))\
         for index, elem in enumerate(content)}      

def run_gui(x,y):
    gui = Constructor_gui(Tk())
    window = gui.windows_constructor('', [392,301,x,y], [False, False],"wheat4")
    
    commands = button_commands_logic(gui, window)
    gui.widgets_creating(commands)
    
    window.protocol("WM_DELETE_WINDOW", lambda: gui.save_content(True))
    window.iconbitmap(f'{os.getcwd()}\\image\\icon.ico')
    gui.mainloop()
    

 