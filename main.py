import math
import re
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from functools import partial
import darkdetect
import threading
import platform
import time
import os
from PIL import Image, ImageDraw
from ast import literal_eval


#GUI SETTINGS-----------------------------------

def on_window_close(event=None):
    global run;run = False


def set_title_theme(window,theme='Light'):

    if OS == 'windows':
        if theme == 'Dark':
            value = 1
        else:
            value = 0

        window.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))

        window.update()
def set_icon_to_window(window):
    if(OS == "windows"):
        window.iconbitmap(f'{runtime_path}/icon.ico')
    elif(OS == "linux"):
        icon_img = PhotoImage(file=f'{runtime_path}/icon.png')
        window.tk.call('wm', 'iconphoto', window._w, icon_img)


class ThemeController:
    def __init__(self,window):
        self.window = window

        if darkdetect.theme() == "Dark":
            set_title_theme(self.window,theme="Dark")
            style.theme_use("darkly")
            self.last_theme = "Dark"
        else:
            style.theme_use("cosmo")
            self.last_theme = "Light" 

        threading.Thread(target=self.check_theme).start()


    def check_theme(self):
        global run
        while run:
            time.sleep(0.05)
            try:
                if darkdetect.theme() == "Dark":
                    if darkdetect.theme() != self.last_theme:
                        set_title_theme(self.window,theme="Dark")
                        style.theme_use("darkly")
                        self.last_theme = "Dark"
                else:
                    if darkdetect.theme() != self.last_theme:
                        set_title_theme(self.window,theme="Light")
                        style.theme_use("cosmo")
                        self.last_theme = "Light"
            except:
                run = False

def center_tk_window(win,window_width,window_height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    win.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
class VerticalScrolledFrame(ttk.Frame):
    # Based on
    # https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        self.vscrollbar = ttk.Scrollbar(self, orient=VERTICAL,bootstyle=("round","ligth"))
        self.vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior,
                                           anchor=NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event=None):
            # Update the scrollbars to match the size of the inner frame.
            root.update()
            self.size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % self.size)
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=self.interior.winfo_reqwidth())
        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event=None):
            root.update()
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)
def call_file_chooser(exten):

    file_chooser_window = Toplevel()
    file_chooser_window.focus()
    file_chooser_window.title("Open file")

    center_tk_window(file_chooser_window,499,400)
    set_title_theme(file_chooser_window,theme=darkdetect.theme())
    file_chooser_window.geometry('500x400')
    file_chooser_window.update()

    file = StringVar()
    file_chooser_window.close_now = False
    file_chooser_window.ready_to_return = False


    top_frame = ttk.Frame(file_chooser_window)
    top_frame.pack()

   
    lbl_location = Label(top_frame,text='Location: ')
    lbl_location.pack(side=LEFT)


    entry_address_bar = ttk.Entry(top_frame)
    entry_address_bar.pack(ipadx=60,pady=5,side=LEFT)

    btn_file_up = ttk.Button(top_frame,bootstyle="secondary",image=folder_up_icon)
    btn_file_up.pack(side=LEFT,padx=5)


    files_label_frame = ttk.LabelFrame(file_chooser_window,text='Open a file:')
    files_label_frame.pack(fill=BOTH,expand=1,padx=50,pady=10)



    files_frame= VerticalScrolledFrame(files_label_frame)
    files_frame.pack(fill=BOTH,expand=1,padx=10,pady=10)
    lisdir_frames = []

    def load_files(path=None):

        if path == None:
            path = os.getcwd()
        else:
            if os.path.isdir(path):
                os.chdir(path)

        if OS == 'windows':
            bf_slash = '\\'    
        elif OS == 'linux':
            bf_slash = '/'
        else:
            bf_slash = '/'

        path = path.replace(f'{bf_slash}{bf_slash}',bf_slash)

        entry_address_bar.delete(0,'end')
        entry_address_bar.insert(0,path)

        files_frame.canvas.yview_moveto(0)

        btn_file_up.config(command=partial(load_files,os.path.abspath('..')))

        for i in lisdir_frames:
            i.destroy()


        list_dir_names  = next(os.walk(path))[1]
        list_file_names = next(os.walk(path))[2]


        def get_file_and_close(file_name):
            file.set(file_name)
            file_chooser_window.close_now = True
            file_chooser_window.ready_to_return = True


        for i in list_dir_names + list_file_names:

            button_frame = ttk.Frame(files_frame.interior)
            button_frame.pack(fill=X,pady=2)

            
            button_frame.button = ttk.Button(button_frame,text='Open',state='disabled')
            button_frame.button.pack(side=LEFT)


            if os.path.isfile(f"{path}{bf_slash}{i}"):
                icon_label = ttk.Label(button_frame,image=file_icon)
            elif os.path.isdir(f"{path}{bf_slash}{i}"):
                icon_label = ttk.Label(button_frame,image=folder_icon)
                button_frame.button.config(state='normal',bootstyle="secondary",command=partial(load_files,f'{path}{bf_slash}{i}'))
            icon_label.pack(side=LEFT,padx=10)

            button_frame_label = ttk.Label(button_frame, text=f"{i}")
            button_frame_label.pack(fill=X)

            if i.endswith(f'{exten}'):
                button_frame.button.config(state='normal',command=partial(get_file_and_close,f"{path}{bf_slash}{i}"))
                icon_label.config(image=wanted_file_icon)
                button_frame_label.config()

            lisdir_frames.append(button_frame)


    def adress_was_chaged(event=None):
        path = entry_address_bar.get()
        if os.path.isdir(path): 
            load_files(entry_address_bar.get())


    entry_address_bar.bind('<Return>',adress_was_chaged)

    load_files()

    file_chooser_window.grab_set()

    #set_icon_to_window(file_chooser_window)

    while not file_chooser_window.close_now and run:
        try:
            time.sleep(0.0001)
            file_chooser_window.update()
        except:
            file_chooser_window.close_now = True
    try:
        file_chooser_window.destroy()
    except:
        pass

    try:
        file_chooser_window.grab_release() 
    except:
        pass

    if file_chooser_window.ready_to_return:
        return file.get()
    else:
        return None
def call_save_as_file(title,exten):

    file_chooser_window = Toplevel()
    file_chooser_window.focus()
    file_chooser_window.title(title)

    center_tk_window(file_chooser_window,499,400)
    set_title_theme(file_chooser_window,theme=darkdetect.theme())
    file_chooser_window.geometry('500x400')
    file_chooser_window.update()

    file = StringVar()
    file.set(exten)

    file_chooser_window.close_now = False
    file_chooser_window.ready_to_return = False


    top_frame = ttk.Frame(file_chooser_window)
    top_frame.pack()

    bottom_frame = ttk.Frame(file_chooser_window)
    bottom_frame.pack(side=BOTTOM)

   
    lbl_location = Label(top_frame,text='Location: ')
    lbl_location.pack(side=LEFT)


    entry_address_bar = ttk.Entry(top_frame)
    entry_address_bar.pack(ipadx=60,pady=5,side=LEFT)

    btn_file_up = ttk.Button(top_frame,bootstyle="secondary",image=folder_up_icon)
    btn_file_up.pack(side=LEFT,padx=5)



    files_label_frame = ttk.LabelFrame(file_chooser_window,text='Create new file in:')
    files_label_frame.pack(fill=BOTH,expand=1,padx=50,pady=10)


    lbl_save_as = Label(bottom_frame,text='Save as: ')
    lbl_save_as.pack(side=LEFT)

    entry_file_name = ttk.Entry(bottom_frame,textvariable=file)
    entry_file_name.pack(ipadx=60,pady=5,side=LEFT)
    entry_file_name.focus()

    
    #'Write the name of the new file.'


    def ready_and_close(event=None):
        if not file.get().endswith(exten) or file.get().replace(" ","").replace(exten,"") == "":
            alert(app_name,f'{exten.upper()} files must have a name\n and end with the extension {exten}')
        else:
            file_chooser_window.ready_to_return =True
            file_chooser_window.close_now = True

    btn_save = ttk.Button(bottom_frame,text=' Save ',command=ready_and_close)
    btn_save.pack(side=LEFT,padx=5)

 
    files_frame= VerticalScrolledFrame(files_label_frame)
    files_frame.pack(fill=BOTH,expand=1,padx=10,pady=10)
    lisdir_frames = []

    def load_files(path=None):

        if path == None:
            path = os.getcwd()
        else: 
            if os.path.isdir(path):
                os.chdir(path)

        if OS == 'windows':
            bf_slash = '\\'    
        elif OS == 'linux':
            bf_slash = '/'
        else:
            bf_slash = '/'

        path = path.replace(f'{bf_slash}{bf_slash}',bf_slash)

        entry_address_bar.delete(0,'end')
        entry_address_bar.insert(0,path)

        files_frame.canvas.yview_moveto(0)

        btn_file_up.config(command=partial(load_files,os.path.abspath('..')))

        for i in lisdir_frames:
            i.destroy()


        list_dir_names  = next(os.walk(path))[1]


        for i in list_dir_names:

            button_frame = ttk.Frame(files_frame.interior)
            button_frame.pack(fill=X,pady=2)


            if os.path.isdir(f"{path}{bf_slash}{i}"):
                icon_label = ttk.Label(button_frame,image=folder_icon)

                button_frame.button = ttk.Button(button_frame,text='Open',bootstyle="secondary",command=partial(load_files,f'{path}{bf_slash}{i}'))
                button_frame.button.pack(side=LEFT)

                
            icon_label.pack(side=LEFT,padx=10)

            button_frame_label = ttk.Label(button_frame, text=f"{i}")
            button_frame_label.pack(fill=X)


            lisdir_frames.append(button_frame)


    def adress_was_chaged(event=None):
        path = entry_address_bar.get()
        if os.path.isdir(path):
            load_files(entry_address_bar.get())


    entry_address_bar.bind('<Return>',adress_was_chaged)
    entry_file_name.bind('<Return>',ready_and_close)


    load_files()

    file_chooser_window.grab_set()

    while not file_chooser_window.close_now and run:
        try:
            time.sleep(0.0001)
            file_chooser_window.update()
        except:
            file_chooser_window.close_now = True
    try:
        file_chooser_window.destroy()
    except:
        pass

    try:
        file_chooser_window.grab_release() 
    except:
        pass


    if file_chooser_window.ready_to_return:
        return file.get()
    else: return None
def askyesno(title,text):
    window = Toplevel()
    window.resizable(0,0)
    center_tk_window(window,299,80)
    set_title_theme(window,theme=darkdetect.theme())
    window.geometry('300x80')
    
    window.title(title)
    
    window.res = 0

    text_label = Label(window,text=text,font= (font,10))
    text_label.pack()
    button_frame = Frame(window)
    button_frame.pack(pady=10)

    def f_yes_and_close():
        window.res = 1
        window.close_now = True
    def f_no_and_close():
        window.res = 0
        window.close_now = True

    btnYes = ttk.Button(button_frame,text='    yes    ',command= f_yes_and_close)
    btnYes.pack(side=LEFT,padx=10)
    btnNo = ttk.Button(button_frame,text='    no    ',command= f_no_and_close)
    btnNo.pack(side=LEFT,padx=10)
    btnYes.focus()

    window.close_now = False


    window.grab_set()

    while not window.close_now:
        try:
            time.sleep(0.0001)
            window.update()
        except:
            window.close_now = True
    try:
        window.destroy()
    except:
        pass

    try:
        window.grab_release() 
    except:
        pass

    return window.res
def alert(title,text,fixed_size=True):
    window = Toplevel()
    if fixed_size:
        window.resizable(0,0)
        center_tk_window(window,299,100)
    set_title_theme(window,theme=darkdetect.theme())
    if fixed_size:
        window.geometry('300x100')
    
    window.title(title)

    text_label = Label(window,text=text)
    text_label.pack(pady=10)
    button_frame = Frame(window)
    button_frame.pack(pady=5)

    def f_okay():
        window.close_now = True
  
    btnOk = ttk.Button(button_frame,text='    Ok    ',command= f_okay)
    btnOk.pack(side=LEFT,padx=10)
    btnOk.focus()

    window.close_now = False

    window.grab_set()

    while not window.close_now:
        try:
            time.sleep(0.0001)
            window.update()
        except:
            window.close_now = True
    try:
        window.destroy()
    except:
        pass

    try:
        window.grab_release() 
    except:
        pass





#---------------------------------------------------








#Color functions
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def calculate_alpha_color(color,bg_color,alpha):
    alpha = alpha/255
    red = color[0] * alpha + bg_color[0] * 1 * (1 - alpha)
    green = color[1] * alpha + bg_color[1] * 1 * (1 - alpha)
    blue = color[2] * alpha + bg_color[2] * 1 * (1 - alpha)
    return (int(red),int(green),int(blue))



class color_class:
    def __init__(self):
        self._rgba_ = [255,255,255,255]

    def set(self,color,color_type="RGBA"):
        if color_type == "hex":
            aux_rgb_color = hex_to_rgb(color)
            self._rgba_ = [aux_rgb_color[0], aux_rgb_color[1], aux_rgb_color[2],self._rgba_[3],]
        elif color_type == "rgb":
            self._rgba_[0]=color[0]
            self._rgba_[1]=color[1]
            self._rgba_[2]=color[2]
        else:
            self._rgba_[0]=color[0]
            self._rgba_[1]=color[1]
            self._rgba_[2]=color[2] 
            self._rgba_[3]=color[3]   

    def setRed(self,red):
        self._rgba_[0] = red

    def getRed(self):
        return self._rgba_[0]

    def setGreen(self,green):
        self._rgba_[1] = green

    def getGreen(self):
        return self._rgba_[1]

    def setBlue(self,blue):
        self._rgba_[2] = blue

    def getBlue(self):
        return self._rgba_[2]

    def set255Alpha(self,alpha):
        self._rgba_[3] = alpha

    def get255Alpha(self):
        return self._rgba_[3]

    def toHex(self):
            return rgb_to_hex((self._rgba_[0],self._rgba_[1],self._rgba_[2]))
    def toRgb(self):
            return (self._rgba_[0],self._rgba_[1],self._rgba_[2])
    def toRgba(self):
            return (self._rgba_[0],self._rgba_[1],self._rgba_[2],self._rgba_[3])
    def get255alpha(self):
            return self._rgba_[3]
    



'''

   rows = 0 
    columns = 0 
    for button_number in amount_rows*amount_columns:
        if columns != amount_columns:
            columns += 1
        else:
            columns = 0
            rows += 1
'''



class class_backup_manager:
    def __init__(self):
        self.backups = []
        self.backup_current_index = -1
    def create_backup(self):
        print("BUCKUP ")
        if self.backup_current_index<9:
            self.backup_current_index += 1
        if len(self.backups) < 10:
            aux_matrix = []
            for row in range(amount_rows):
                aux_matrix.append(matrix[row].copy())
            self.backups.append(aux_matrix)
        else:
            aux_matrix = []
            for row in range(amount_rows):
                aux_matrix.append(matrix[row].copy())
            self.backups.append(aux_matrix)
            del self.backups[0]
    def load_backup_to_canvas(self):
        #print(self.backup_current_index)
        mtx = self.backups[self.backup_current_index]
        print(self.backup_current_index)

        global matrix; matrix = mtx

        if self.backup_current_index > 0:
            del self.backups[self.backup_current_index]

        if self.backup_current_index >0:
            self.backup_current_index = self.backup_current_index -1
        button_number = 0
        for row in range(amount_rows):
            for column in range(amount_columns):
                button_number += 1

                if not button_number % 2 == 0:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( mtx[row][column][0:3] ,hex_to_rgb("#222222"),mtx[row][column][3]))
                else:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( mtx[row][column][0:3] ,hex_to_rgb("#333333"),mtx[row][column][3]))

                canvas.itemconfig(button_number, fill= aux_hex_color,outline =aux_hex_color  )
    def load_from_matrix(self,mtx):
        button_number = 0
        for row in range(amount_rows):
            for column in range(amount_columns):
                button_number += 1

                if not button_number % 2 == 0:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( mtx[row][column][0:3] ,hex_to_rgb("#222222"),mtx[row][column][3]))
                else:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( mtx[row][column][0:3] ,hex_to_rgb("#333333"),mtx[row][column][3]))

                canvas.itemconfig(button_number, fill= aux_hex_color,outline =aux_hex_color  )        











def update_current_color_preview():
    color_label.set( f"{CURRENT_COLOR.toHex()}\nrgb{CURRENT_COLOR.toRgb() }" )
    aux_rgb_color = CURRENT_COLOR.toRgb()
    if CURRENT_COLOR.getRed() + CURRENT_COLOR.getGreen() + CURRENT_COLOR.getBlue() > 200:
        color_select["fg"] = "#000"
    else:
        color_select["fg"] = "#fff"
    color_select.config(bg=CURRENT_COLOR.toHex())





def colors_on_mouse_drag(event):
    """Mouse movement callback"""
    # get mouse coordinates
    x = event.x
    y = event.y
    # clear the canvas_of_colors and redraw
    canvas_of_colors.delete("all")
    canvas_of_colors.create_image(size_of_color_palette[0]/2, size_of_color_palette[1]/2, image=color_palette)
    canvas_of_colors.create_image(x, y, image=target)
    
    if x < size_of_color_palette[0] and x >0 and y < size_of_color_palette[1] and y >0: 
        rgb_color = color_palette.get(x, y)
        CURRENT_COLOR.set(rgb_color,"rgb")
        update_current_color_preview()
        scl_red.set(CURRENT_COLOR.getRed())
        scl_green.set(CURRENT_COLOR.getGreen())
        scl_blue.set(CURRENT_COLOR.getBlue())


def fill_with_color(row,column):
    sqs_to_fill = []
    sqs_to_fill.append((row,column))

    old_color = matrix[row-1][column-1]

    if old_color == CURRENT_COLOR.toRgba():
        return

    while(len(sqs_to_fill) != 0):
        row = sqs_to_fill[0][0]
        column = sqs_to_fill[0][1]
        del sqs_to_fill[0]

        button_number = (row -1)*amount_columns + column

        if row <= amount_rows and row >0 and column <= amount_columns and column >0:
            if not ( old_color[3]==0 and CURRENT_COLOR.get255Alpha() == 0):
                if  matrix[row-1][column-1] == old_color or (matrix[row-1][column-1][3] == 0 and old_color[3] == 0)  :
                    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', CURRENT_COLOR.toHex()) and len(CURRENT_COLOR.toHex()) == 7:
                        if CURRENT_COLOR.get255Alpha() != 0:
                            matrix[row-1][column-1] =  CURRENT_COLOR.toRgba()
                        else:
                            matrix[row-1][column-1] = (0,0,0,0)
                        if not button_number % 2 == 0:
                            aux_hex_color = rgb_to_hex(  calculate_alpha_color( CURRENT_COLOR.toRgb() ,hex_to_rgb("#222222"),CURRENT_COLOR.get255Alpha()))
                        else:
                            aux_hex_color = rgb_to_hex(  calculate_alpha_color( CURRENT_COLOR.toRgb() ,hex_to_rgb("#333333"),CURRENT_COLOR.get255Alpha()))
                        canvas.itemconfig(button_number, fill= aux_hex_color,outline =aux_hex_color  )
                        sqs_to_fill.append((row,column-1))
                        sqs_to_fill.append((row,column+1))
                        sqs_to_fill.append((row-1,column))
                        sqs_to_fill.append((row+1,column))
                    else:
                        alert("Error","please write a valid hex color.")



def fill_with_color_function_event(event=None):
    button_number = (row -1)*amount_columns + column
    
    if row <= amount_rows and row >0 and column <= amount_columns and column >0: 
        if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', CURRENT_COLOR.toHex()) and len(CURRENT_COLOR.toHex()) == 7:
            fill_with_color(row,column)
        else:
            alert("Error","please write a valid hex color.")







def fill_with_color_even_sqs(row,column):
    sqs_to_fill = []
    sqs_to_fill.append((row,column))

    old_color = matrix[row-1][column-1]

    if old_color == CURRENT_COLOR.toRgba():
        return

    while(len(sqs_to_fill) != 0):
        row = sqs_to_fill[0][0]
        column = sqs_to_fill[0][1]
        del sqs_to_fill[0]

        button_number = (row -1)*amount_columns + column

        if row <= amount_rows and row >0 and column <= amount_columns and column >0:
            if not ( old_color[3]==0 and CURRENT_COLOR.get255Alpha() == 0):
                if  matrix[row-1][column-1] == old_color or (matrix[row-1][column-1][3] == 0 and old_color[3] == 0)  :
                    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', CURRENT_COLOR.toHex()) and len(CURRENT_COLOR.toHex()) == 7:
                        aux_bn = (row -1)*amount_columns + column

                        if aux_bn % 2 == 0:
                            if CURRENT_COLOR.get255Alpha() != 0:
                                matrix[row-1][column-1] =  CURRENT_COLOR.toRgba()
                            else:
                                matrix[row-1][column-1] = (0,0,0,0)
                            if not button_number % 2 == 0:
                                aux_hex_color = rgb_to_hex(  calculate_alpha_color( CURRENT_COLOR.toRgb() ,hex_to_rgb("#222222"),CURRENT_COLOR.get255Alpha()))
                            else:
                                aux_hex_color = rgb_to_hex(  calculate_alpha_color( CURRENT_COLOR.toRgb() ,hex_to_rgb("#333333"),CURRENT_COLOR.get255Alpha()))
                            canvas.itemconfig(button_number, fill= aux_hex_color,outline =aux_hex_color  )
                        sqs_to_fill.append((row,column-1))
                        sqs_to_fill.append((row,column+1))
                        sqs_to_fill.append((row-1,column))
                        sqs_to_fill.append((row+1,column))
                    else:
                        alert("Error","please write a valid hex color.")



def fill_with_color_even_sqs_function_event(event=None):
    button_number = (row -1)*amount_columns + column
    
    if row <= amount_rows and row >0 and column <= amount_columns and column >0: 
        if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', CURRENT_COLOR.toHex()) and len(CURRENT_COLOR.toHex()) == 7:
            fill_with_color_even_sqs(row,column)
        else:
            alert("Error","please write a valid hex color.")




def point_selection(event=None):
    if row <= amount_rows and row >0 and column <= amount_columns and column >0: 

        for i in range(1,amount_rows*amount_columns):
            if canvas.itemcget(i, "fill") == "#000" and canvas.itemcget(i, "outline") == "#fff":
                pass

        button_number = (row -1)*amount_columns + column
        canvas.itemconfig(button_number, fill= "#000",outline="#fff"  )
  




def clicked_canvas_button1(event):
    update_mouse_position(event)
    mouse_position.set(f"x:{column} y:{row}")
    if row <= amount_rows and row >0 and column <= amount_columns and column >0: 

        if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$',CURRENT_COLOR.toHex()) and len(CURRENT_COLOR.toHex()) == 7:
            matrix[row-1][column-1] =  CURRENT_COLOR.toRgba()
            # n = (f-1)20 + c
            button_number = (row -1)*amount_columns + column
            if not button_number % 2 == 0:
                aux_hex_color = rgb_to_hex(  calculate_alpha_color( CURRENT_COLOR.toRgb() ,hex_to_rgb("#222222"),CURRENT_COLOR.get255Alpha()  ) )
            else:
                aux_hex_color = rgb_to_hex(  calculate_alpha_color( CURRENT_COLOR.toRgb() ,hex_to_rgb("#333333"),CURRENT_COLOR.get255Alpha()  ) )
            canvas.itemconfig(button_number, fill= aux_hex_color,outline=aux_hex_color  )
        else:
            alert("Error","please write a valid hex color.")


def clicked_canvas_button3(event):
    update_mouse_position(event)
    mouse_position.set(f"x:{column} y:{row}")

    button_number = (row -1)*amount_columns + column
    

    if row <= amount_rows and row >0 and column <= amount_columns and column >0: 
        matrix[row-1][column-1] =  (0,0,0,0)
        if not button_number % 2 == 0:
            canvas.itemconfig(button_number, fill="#222",outline="#222")
        else:
            canvas.itemconfig(button_number, fill="#333",outline="#333")
 
    
def update_mouse_position(event=None):
    global column;column = math.ceil(event.x/sq_size)
    global row;row       = math.ceil(event.y/sq_size)
    global button_number
    mouse_position.set(f"x:{column} y:{row}")


def pick_color(event=None):
    if matrix[row-1][column-1][3]>0:
        CURRENT_COLOR.set(matrix[row-1][column-1])
        update_current_color_preview()
        scl_alpha.set(CURRENT_COLOR.get255Alpha() )
        lbl_alpha_value.config(text=CURRENT_COLOR.get255Alpha() )
        scl_red.set(CURRENT_COLOR.getRed())
        scl_green.set(CURRENT_COLOR.getGreen())
        scl_blue.set(CURRENT_COLOR.getBlue())




def fn_key_pressed(event):
    global matrix

    if event.keysym == "f":
        fill_with_color_function_event()
    if event.keysym == "e":
        fill_with_color_even_sqs_function_event()

    if event.keysym == "p":
        pick_color()

    if event.keysym == "s":
        backup_manager.create_backup()

    if event.keysym == "z":
        #point_selection()
        backup_manager.load_backup_to_canvas()



        
    if event.keysym == "q":
        pass

    if event.keysym == "w":
        pass
 

    
    if event.keysym == "Left":
        for button_number in canvas.find_all():
            canvas.move(button_number,50,0)
    elif event.keysym == "Right":
        for button_number in canvas.find_all():
            canvas.move(button_number,-50,0)    
    elif event.keysym == "Up":
        for button_number in canvas.find_all():
            canvas.move(button_number,0,50)    
    elif event.keysym == "Down":
        for button_number in canvas.find_all():
            canvas.move(button_number,0,-50)    
    root.update()


def fn_darker_color():
    var_new_rgb_color = []
    for i in CURRENT_COLOR.toRgb():
        if i - 5 >= 0:
            var_new_rgb_color.append(i -5)
        else:
            var_new_rgb_color.append(0)
    CURRENT_COLOR.set(var_new_rgb_color,"rgb")

    color_label.set( f"{CURRENT_COLOR.toHex()}\nrgb{CURRENT_COLOR.toRgb() }" )  
    color_select['bg'] = CURRENT_COLOR.toHex()

    scl_red.set(CURRENT_COLOR.getRed())
    scl_green.set(CURRENT_COLOR.getGreen())
    scl_blue.set(CURRENT_COLOR.getBlue())

def fn_brighter_color():
    var_new_rgb_color = []
    for i in CURRENT_COLOR.toRgb():
        if i + 5 <= 255:
            var_new_rgb_color.append(i +5)
        else:
            var_new_rgb_color.append(255)
    CURRENT_COLOR.set(var_new_rgb_color,"rgb")

    color_label.set( f"{CURRENT_COLOR.toHex()}\nrgb{CURRENT_COLOR.toRgb() }" )  
    color_select['bg'] = CURRENT_COLOR.toHex()

    scl_red.set(CURRENT_COLOR.getRed())
    scl_green.set(CURRENT_COLOR.getGreen())
    scl_blue.set(CURRENT_COLOR.getBlue())









OS = platform.platform().split("-")[0].lower()

if OS == 'windows':
    import ctypes as ct
    font = 'Comic Sans MS'
else:
    font = 'Areal'


run = True
app_name = 'PixPynter'


home = os.path.expanduser("~")  #file_path a Home

runtime_path = f"{os.path.dirname(os.path.realpath(__file__))}/appdata" #file_path en donde se descomprime y ejecuta 
app_folder_path = f"{home}/.{app_name}-config"                            #file_path en donde se guarda las cosas de la app (en la carpeta del usuario)




#Create the window
root = ttk.Window(themename="darkly")
root.title(app_name)
root.geometry("1000x900")

style = ttk.Style()



#Start Theme controller
ThemeController(root)
root.update()
root.state("zoomed")



#load icons
file_icon = PhotoImage(file=f'{runtime_path}/images/file.png')
wanted_file_icon = PhotoImage(file=f'{runtime_path}/images/wanted_file.png')
folder_icon = PhotoImage(file=f'{runtime_path}/images/folder.png')
folder_up_icon = PhotoImage(file=f'{runtime_path}/images/folder_up.png')





left_frame = ttk.LabelFrame(text="Pick a color!")
left_frame.pack(side=LEFT,fill=Y,pady=30,padx=30)

colors_frame = Frame(left_frame)
colors_frame.pack()


brightness_frame = ttk.LabelFrame(left_frame,text="Brightness")
brightness_frame.pack(fill=X,padx=20,pady=10)

ttk.Button(brightness_frame,text="Darker",command=fn_darker_color,bootstyle="secondary").pack(side=LEFT,fill=X,expand=1,padx=5,pady=5)
ttk.Button(brightness_frame,text="Brighter",command=fn_brighter_color,bootstyle="secondary").pack(side=LEFT,fill=X,expand=1,padx=5,pady=5)



CURRENT_COLOR = color_class()




GLOBAL_BG_COLOR = StringVar()
GLOBAL_BG_COLOR.set("#222222")

size_of_color_palette = (509,298)
        
color_label = StringVar()
color_label.set('#ffffff\nrgb(255,255,255)')
color_select = Label(colors_frame, textvariable=color_label, bg='white',fg="black", width=20, font=('Arial', 20, 'bold'))
color_select.pack( fill=X,pady=10,padx=20)    
canvas_of_colors = Canvas(colors_frame, height=298, width=509,cursor="crosshair",bg="#222",relief='ridge',bd=0,highlightthickness=0)
canvas_of_colors.pack(side=LEFT,padx=20)
canvas_of_colors.bind("<B1-Motion>", colors_on_mouse_drag)
canvas_of_colors.bind("<Button-1>", colors_on_mouse_drag)



color_palette = PhotoImage(file=f'{runtime_path}/images/colors.png')
target = PhotoImage(file=f'{runtime_path}/images/target.png')

canvas_of_colors.create_image(size_of_color_palette[0]/2, size_of_color_palette[1]/2, image=color_palette)
canvas_of_colors.create_image(50, 10, image=target)



#hex_color_entry= ttk.Entry(left_frame,textvariable=GLOBAL_COLOR)
#hex_color_entry.pack(fill=X,pady=10,padx=20)




red_control_frame = ttk.LabelFrame(left_frame,text="Red:")
red_control_frame.pack(fill=X,padx=20)

green_control_frame = ttk.LabelFrame(left_frame,text="Green:")
green_control_frame.pack(fill=X,padx=20)

blue_control_frame = ttk.LabelFrame(left_frame,text="Blue:")
blue_control_frame.pack(fill=X,padx=20)


alpha_control_frame = ttk.LabelFrame(left_frame,text="alpha:")
alpha_control_frame.pack(fill=X,padx=20)


lbl_red_value = Label(red_control_frame,text="")
lbl_red_value.pack(fill=X)

lbl_green_value = Label(green_control_frame,text="")
lbl_green_value.pack(fill=X)

lbl_blue_value = Label(blue_control_frame,text="")
lbl_blue_value.pack(fill=X)

lbl_alpha_value = Label(alpha_control_frame,text="")
lbl_alpha_value.pack(fill=X)




def change_red(event=None):
    CURRENT_COLOR.setRed(int(scl_red.get())) 
    lbl_red_value.config(text=CURRENT_COLOR.getRed())
    update_current_color_preview()

def change_green(event=None):
    CURRENT_COLOR.setGreen(int(scl_green.get())) 
    lbl_green_value.config(text=CURRENT_COLOR.getGreen())
    update_current_color_preview()


def change_blue(event=None):
    CURRENT_COLOR.setBlue(int(scl_blue.get())) 
    lbl_blue_value.config(text=CURRENT_COLOR.getBlue())
    update_current_color_preview()


def change_alpha(event=None):
    CURRENT_COLOR.set255Alpha(int(scl_alpha.get())) 
    if CURRENT_COLOR.get255Alpha()>0:
        lbl_alpha_value.config(text=CURRENT_COLOR.get255Alpha())
    else:
        lbl_alpha_value.config(text=f"{CURRENT_COLOR.get255Alpha()} #Now you can remove pixels")


scl_red = ttk.Scale(red_control_frame, from_=0, to=255, orient=HORIZONTAL, command=change_red)
scl_red.set(255)
scl_red.pack(fill=X)


scl_green = ttk.Scale(green_control_frame, from_=0, to=255, orient=HORIZONTAL, command=change_green)
scl_green.set(255)
scl_green.pack(fill=X)

scl_blue = ttk.Scale(blue_control_frame, from_=0, to=255, orient=HORIZONTAL, command=change_blue)
scl_blue.set(255)
scl_blue.pack(fill=X)


scl_alpha = ttk.Scale(alpha_control_frame, from_=0, to=255, orient=HORIZONTAL, command=change_alpha)
scl_alpha.set(255)
scl_alpha.pack(fill=X)







mouse_position = StringVar()
mouse_position.set('x:?   y:?')
lbl_mouse_position = Label(textvariable=mouse_position)
lbl_mouse_position.pack()




frame=Frame(root,width=300,height=300)
frame.pack(expand=True, fill=BOTH) 
canvas=ttk.Canvas(frame,bg='#000000',width=1000, height=1000,cursor="crosshair")
canvas.pack(side=LEFT,expand=True,fill=BOTH)


amount_rows=65
amount_columns=85
sq_size =15
row = 1
column =1

matrix = []

backup_manager = class_backup_manager()



#Create matrix for the image
for f in range(amount_rows):
    matrix = matrix + [[]]

for c in matrix:
    for f in range(amount_columns):
        c.append((0,0,0,0))

x = 0
y = 0


#Create the canvas for drawing 
even_sq = 0
for f in range(amount_rows):
    x = -sq_size
    for c in range(amount_columns):
        x += sq_size
        even_sq = not even_sq
        if even_sq:
            button_number = canvas.create_rectangle(x, y, x+sq_size-1,y+sq_size-1, fill="#222", outline = '#222')
        else:
            button_number = canvas.create_rectangle(x, y, x+sq_size-1,y+sq_size-1, fill="#333", outline = '#333')
    y += sq_size


def show_image():
    img = Image.new("RGBA", (len(matrix[1])*sq_size+2, len(matrix)*sq_size +2))
    draw = ImageDraw.Draw(img)
    x = 0
    y = 0

    #---------------
    '''  This block should be able to crop the image automatically. (Not ready)
    
    aux_matrix = []
    for f in matrix:
        row_transparente = True
        for c in f:
            if c[3] > 0:
                row_transparente = False
        if not row_transparente:
            aux_matrix.append(f)

    aux_aux_matrix= []




    

    for f in range(len(aux_matrix[0])):
        aux_aux_matrix = aux_aux_matrix + [[]]

    for f in aux_matrix:
        for c in f:

    for c in matrix:
        for f in range(amount_columns):
            c.append((0,0,0,0))

    


    
    
    column_transparente = True
    for c in range(len(aux_matrix[0])-1):
        for f in range(len(aux_matrix)-1):
            print(f"f:{f}")
            print(f"c:{c}")
            print(aux_matrix[f])
            if aux_matrix[f][c][3] > 0 :
                column_transparente = False
        if not column_transparente:
            for f in range(len(aux_matrix)-1):
                del aux_matrix[f][c]
    '''
    #-----------------

    for f in matrix:
        x = -sq_size
        for c in f:
            x += sq_size
            if c[3] > 0:
                draw.rectangle((x, y, x+sq_size-1, y+sq_size-1), fill=c)
        y += sq_size

    img.show()


def fn_save_as_png():
    img = Image.new("RGBA", (len(matrix[1])*sq_size+2, len(matrix)*sq_size +2))
    draw = ImageDraw.Draw(img)
    x = 0
    y = 0

    for f in matrix:
        x = -sq_size
        for c in f:
            x += sq_size
            if c[3] > 0:
                draw.rectangle((x, y, x+sq_size-1, y+sq_size-1), fill=c)

        y += sq_size
    file_name = call_save_as_file("Save as a png file:",".png")
    if file_name != None:

        img.save(file_name)


def save_file():
    file_name = call_save_as_file("Save:",".pxpf")
    if file_name != None:
        # writing matrix to a file
        with open(file_name, 'w') as file:
            file.write(str(matrix))
        alert(app_name,"Saved")

def load_file():
    global matrix
    file_name = call_file_chooser(".pxpf")
    if file_name != None:
        with open(file_name,"r") as file:
            matrix = literal_eval(file.read())

        backup_manager.load_from_matrix(matrix)
        alert(app_name,"Loaded")




btn_show_img = ttk.Button(left_frame,text="Image Preview",command=show_image,bootstyle="secondary")
btn_show_img.pack(pady=20)

btn_save_as = ttk.Button(left_frame,text="Export as png",command=fn_save_as_png,bootstyle="secondary")
btn_save_as.pack(pady=20)




btn_save_to_file = ttk.Button(left_frame,text="Save",command=save_file,bootstyle="secondary")
btn_save_to_file.pack(pady=20)


btn_load_file = ttk.Button(left_frame,text="Open",command=load_file,bootstyle="secondary")
btn_load_file.pack(pady=20)




def fn_show_instructions():
    var_instructions = '''


        Hi, thanks for trying the program.

        These are the keys and tool combinations:

        =========================================
        Click - Draw

        Right click - delete

        P - Pick color

        F - fill with color

        mouse wheel click - fill with color

        E - Fill with color only the even squares

        ==========================================

        We are open to suggestions and more developers 
        who want to contribute to the project.


    '''
    alert("Instructions",var_instructions,fixed_size=False)

ttk.Button(left_frame,text="Instructions (How to use)",command=fn_show_instructions).pack()




#Events
canvas.bind("<Button-1>", clicked_canvas_button1)
canvas.bind("<B1-Motion>", clicked_canvas_button1)
canvas.bind("<Button-3>", clicked_canvas_button3)
canvas.bind("<B3-Motion>", clicked_canvas_button3)
canvas.bind("<Motion>",update_mouse_position)
root.bind("<Button-2>",fill_with_color_function_event)
root.bind("<Key>",fn_key_pressed)





root.bind('<Destroy>',on_window_close)
root.mainloop()





