from settings import *

from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from functools import partial
import darkdetect
import threading
import platform
import time




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
    def __init__(self,window,style):
        self.window = window
        self.style = style

        self.dark_theme_name = "darkly"
        self.light_theme_name = "cosmo"

        if darkdetect.theme() == "Dark":
            set_title_theme(self.window,theme="Dark")
            self.style.theme_use(self.dark_theme_name)
            self.last_theme = "Dark"
        else:
            self.style.theme_use(self.light_theme_name)
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
                        self.style.theme_use(self.dark_theme_name)
                        self.last_theme = "Dark"
                else:
                    if darkdetect.theme() != self.last_theme:
                        set_title_theme(self.window,theme="Light")
                        self.style.theme_use(self.light_theme_name)
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
            #root.update()
            self.size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % self.size)
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=self.interior.winfo_reqwidth())
        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event=None):
            #root.update()
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)
def call_file_chooser(exten):

    file_chooser_window = Toplevel()
    file_chooser_window.focus()
    file_chooser_window.title("Open file")



    #load icons
    file_icon = PhotoImage(file=f'{runtime_path}/images/file.png')
    wanted_file_icon = PhotoImage(file=f'{runtime_path}/images/wanted_file.png')
    folder_icon = PhotoImage(file=f'{runtime_path}/images/folder.png')
    folder_up_icon = PhotoImage(file=f'{runtime_path}/images/folder_up.png')


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



    #load icons
    file_icon = PhotoImage(file=f'{runtime_path}/images/file.png')
    wanted_file_icon = PhotoImage(file=f'{runtime_path}/images/wanted_file.png')
    folder_icon = PhotoImage(file=f'{runtime_path}/images/folder.png')
    folder_up_icon = PhotoImage(file=f'{runtime_path}/images/folder_up.png')


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






def call_size_chooser():

    size_chooser_window = Toplevel()
    size_chooser_window.focus()
    size_chooser_window.title("Open file")

    center_tk_window(size_chooser_window,499,400)
    set_title_theme(size_chooser_window,theme=darkdetect.theme())
    size_chooser_window.geometry('500x400')
    size_chooser_window.update()

    
    sq_size = 1


    size_chooser_window.close_now = False
    size_chooser_window.ready_to_return = False


    top_frame = ttk.Frame(size_chooser_window)
    top_frame.pack()

   
    lbl_size = Label(top_frame,text='Size: ')
    lbl_size.pack(side=LEFT)


    def change_image_preview(event=None):
        str_size = entry_size.get()
        if str_size != '':
            size = int(str_size)
        else:
            size = 1
        current_image = create_png_from_matrix(matrix,size)
        img_previw = ImageTk.PhotoImage(current_image)
        current_image.show()
        lbl_image.config(image=img_previw)






    entry_size = ttk.Entry(top_frame)
    entry_size.pack(ipadx=60,pady=5,side=LEFT)

    entry_size.bind("<KeyPress>",change_image_preview)



    current_image = create_png_from_matrix(matrix,1)
    img_previw = ImageTk.PhotoImage(current_image)

    lbl_image = Label(size_chooser_window,image=img_previw)
    lbl_image.pack(expand=1,fill=BOTH)

    


    size_chooser_window.grab_set()


    while not size_chooser_window.close_now and run:
        try:
            time.sleep(0.0001)
            size_chooser_window.update()
        except:
            size_chooser_window.close_now = True
    try:
        size_chooser_window.destroy()
    except:
        pass

    try:
        size_chooser_window.grab_release() 
    except:
        pass

    if size_chooser_window.ready_to_return:
        return sq_size
    else:
        return None


