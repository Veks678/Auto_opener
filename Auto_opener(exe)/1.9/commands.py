# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
import os

from psutil import process_iter
import win32com.client
import webbrowser
import time


class button_commands_logic():
    def __init__(self, gui, window):
        self.gui, self.window = gui, window   
    
#-------------------------------------------------------------------------------------     
    def delete_elem(self, widget):
        index = list(self.gui.info_button.keys()).index(widget)
        field_get = self.gui.text_field[0].get(index)

        if field_get in self.gui.info_programm:
            with os.scandir(self.gui.shortcuts_path) as direct:
                {os.remove(self.gui.info_programm[field_get][0]) for file in direct\
                 if file.name == field_get}

            del self.gui.info_programm[field_get]

        del self.gui.info_button[widget]
        self.gui.text_field[0].delete(index)    
        widget.destroy()

        for i, elem in enumerate(self.gui.info_button):
            if i > index-1:
                self.gui.info_button[elem] -= 20
                elem.place_configure(y = self.gui.info_button[elem])

#-------------------------------------------------------------------------------------    
    def adding_elem(self, pressing=True):
        if (20 * len(self.gui.info_button) + 28) == 248:
            return 
        elif pressing == True:
            text_get = self.gui.text_field[-1].get('1.0', 'end-1c')
            
            if len(text_get) == 0:
                return
            elif os.path.isfile(text_get) == True: 
                programm_name = ''.join(text_get.split('\\')[-1:])[0:-4].rstrip('.')
                shortcut = win32com.client.Dispatch("WScript.Shell").CreateShortCut(\
                    (f'{self.gui.shortcuts_path}\\{programm_name}.lnk')\
                )
                shortcut.Targetpath = text_get
                shortcut.save()
                self.gui.save_content()

            elif os.path.isfile(text_get) == False:
                self.gui.text_field[0].insert(\
                    END, self.gui.text_field[-1].get('1.0','end-1c')\
                )
            else:
                return
            
            self.gui.text_field[-1].delete('0.0', END)                
             
        y = (20 * (len(self.gui.info_button)+ 1)) + 28
        widget = self.gui.widgets_constructor(Button, "gray25", "white")
        widget.config(image=self.gui.clear_img, command=lambda: self.delete_elem(widget))
        widget.place(x = 368, y = y, height = 20, width = 20) 
        
        self.gui.info_button[widget] = y    
#-------------------------------------------------------------------------------------     
    def Open(self):
        for elem in list(self.gui.text_field[0].get(0, END)) :
            if '/' in elem:
                webbrowser.open_new_tab(elem)  
                
            elif ':' in elem[0:3]:
                os.startfile(os.path.realpath(elem))
                
            elif self.gui.info_programm[elem][0][-4:] == '.lnk':   
                if len(self.gui.info_programm[elem])-1 == 0:
                    init_p = {p.info['name'] for p in process_iter(['name'])}
                    os.startfile(self.gui.info_programm[elem][0])
                    final_p = {p.info['name'] for p in process_iter(['name'])}
                    
                    if len(list(final_p.difference(init_p))) > 0:
                        self.gui.info_programm[elem].append(\
                            list(final_p.difference(init_p))[0])  
                else:
                    if self.gui.process_status(self.gui.info_programm[elem][1]) == 0:
                        os.startfile(self.gui.info_programm[elem][0])
            
            time.sleep(0.3)        
        
        self.gui.save_content()
            
#-------------------------------------------------------------------------------------         
    def Close(self):
        for elem in self.gui.info_programm:
            if len(self.gui.info_programm[elem])-1 == 1:
                if self.gui.process_status(self.gui.info_programm[elem][1]) == 1: 
                    
                    {proc.kill() for proc in process_iter()\
                     if proc.name() == self.gui.info_programm[elem][1]}
                    
                    del self.gui.info_programm[elem][1]
                else:
                    del self.gui.info_programm[elem][1]

            time.sleep(0.3)   
        
        self.gui.save_content()
                        
                