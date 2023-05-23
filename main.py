import random
import math
import re
import time
import os


from gui import *
from funcs_and_classes import *






#Create the window
root = ttk.Window(themename="")
root.title(f"{app_name}-{version}")
root.geometry("1000x900")

#Create style 
style = ttk.Style()

#Start Theme controller
ThemeController(root,style) 
root.update()
root.state("zoomed")



#icon_fill_tool = PhotoImage(file=f'{runtime_path}/images/fill-drip-solid.png')
#icon_brush_tool = PhotoImage(file=f'{runtime_path}/images/paint-brush-solid.png')
#icon_color_picker_tool = PhotoImage(file=f'{runtime_path}/images/eye-dropper-solid.png')






#UI VARIABLES:
CURRENT_COLOR = color_class()


canvas_bg_dark_colors =["#222222","#333333"]
canvas_bg_light_colors =["#a0a0a0","#aaaaaa"]



size_of_color_palette = (373,219)
color_label = StringVar()
color_palette = PhotoImage(file=f'{runtime_path}/images/colors.png')
target = PhotoImage(file=f'{runtime_path}/images/target.png')

tool_type = "draw_pixel"


left_frame = ttk.LabelFrame(root,text="Pick a nice color!")
left_frame.pack(side=LEFT,fill=Y,pady=15,padx=20)

colors_frame = Frame(left_frame)
colors_frame.pack()

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

brightness_frame = ttk.LabelFrame(left_frame,text="Brightness")
brightness_frame.pack(padx=20,pady=10,fill=X)

ttk.Button(brightness_frame,text="Darker",command=fn_darker_color,bootstyle="secondary").pack(side=LEFT,fill=X,expand=1,padx=5,pady=5)
ttk.Button(brightness_frame,text="Brighter",command=fn_brighter_color,bootstyle="secondary").pack(side=LEFT,fill=X,expand=1,padx=5,pady=5)

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



color_label.set('#ffffff\nrgb(255,255,255)')
color_select = Label(colors_frame, textvariable=color_label, bg='white',fg="black", width=20, font=('Arial', 20, 'bold'))
color_select.pack(pady=10,padx=23,fill=X)    
canvas_of_colors = Canvas(colors_frame, height=220, width=380,cursor="crosshair",bg="#222",relief='ridge',bd=0,highlightthickness=0)
canvas_of_colors.pack(side=LEFT,padx=20)
canvas_of_colors.bind("<B1-Motion>", colors_on_mouse_drag)
canvas_of_colors.bind("<Button-1>", colors_on_mouse_drag)

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

def update_current_color_preview():
    color_label.set( f"{CURRENT_COLOR.toHex()}\nrgb{CURRENT_COLOR.toRgb() }" )
    aux_rgb_color = CURRENT_COLOR.toRgb()
    if CURRENT_COLOR.getRed() + CURRENT_COLOR.getGreen() + CURRENT_COLOR.getBlue() > 200:
        color_select["fg"] = "#000"
    else:
        color_select["fg"] = "#fff"
    color_select.config(bg=CURRENT_COLOR.toHex())

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



def fn_key_pressed(event):

    global tool_type

    key = event.keysym.lower()

    if key == "s":
        tool_type ="selection_tool"


    if key == "1" or key == "d":
        tool_type = 'draw_pixel'

    if key == "2" or key == "f":
        tool_type = "fill_canvas_with_color"

    if key == "3" or key == "p":
        tool_type = "pick_color"

    if key == "z":
        pass
        #backup_manager.load_backup_to_canvas()

    if key == "x":
        root.destroy()

    update_tool_button_colors()


#WORKING ON


def update_tool_button_colors():
    if tool_type == "draw_pixel":
        button_set_tool_draw_pixel.config(bootstyle="primary")
    else:
        button_set_tool_draw_pixel.config(bootstyle="secondary")

    if tool_type == "fill_canvas_with_color":
        button_set_tool_fill_canvas_with_color.config(bootstyle="primary")
    else:
        button_set_tool_fill_canvas_with_color.config(bootstyle="secondary")

    if tool_type == "pick_color":
        button_set_tool_pick_color.config(bootstyle="primary")
    else:
        button_set_tool_pick_color.config(bootstyle="secondary")

    if tool_type == "selection_tool":
        button_set_tool_selection_tool.config(bootstyle="primary")
    else:
        button_set_tool_selection_tool.config(bootstyle="secondary")




def set_tool_type_to_draw_pixel():global tool_type;tool_type = "draw_pixel";update_tool_button_colors()
def set_tool_type_to_fill_canvas_with_color():global tool_type;tool_type = "fill_canvas_with_color";update_tool_button_colors()
def set_tool_type_to_pick_color():global tool_type;tool_type = "pick_color";update_tool_button_colors()
def set_tool_type_to_selection_tool():global tool_type;tool_type = "selection_tool";update_tool_button_colors()

def image_preview():
    for i in tab_with_canvas_list:
        if i.is_canvas_active():
            i.image_preview()

def export_as_png_file():
    for i in tab_with_canvas_list:
        if i.is_canvas_active():
            i.export_as_png_file()

def save_to_file():
    for i in tab_with_canvas_list:
        if i.is_canvas_active():
            i.save_to_file()


tools_frame = ttk.LabelFrame(left_frame,text="Here are your tools!")
tools_frame.pack(fill=BOTH,padx=20,pady=20)

button_set_tool_draw_pixel = ttk.Button(tools_frame,text="draw_pixel",command=set_tool_type_to_draw_pixel)
button_set_tool_draw_pixel.grid(row = 0, column = 0, padx = 5,pady = 5)

button_set_tool_fill_canvas_with_color = ttk.Button(tools_frame,text="fill_canvas_with_color",command=set_tool_type_to_fill_canvas_with_color)
button_set_tool_fill_canvas_with_color.grid(row = 0, column = 1, padx = 20,pady = 5)


button_set_tool_pick_color = ttk.Button(tools_frame,text="pick_color", command=set_tool_type_to_pick_color)
button_set_tool_pick_color.grid(row = 0, column = 2, padx = 5,pady = 5)

button_set_tool_selection_tool  = ttk.Button(tools_frame,text="selection_tool", command=set_tool_type_to_selection_tool)
button_set_tool_selection_tool.grid(row = 2, column = 0, padx = 5,pady = 5)


button_image_preview = ttk.Button(left_frame,bootstyle="secondary",text="image_preview", command=image_preview)
button_image_preview.pack(fill="x", padx = 20,pady = 5)


button_export_as_png_file = ttk.Button(left_frame,bootstyle="secondary",text="export_as_png_file", command=export_as_png_file)
button_export_as_png_file.pack(fill="x", padx = 20,pady = 5)


button_save_to_file = ttk.Button(left_frame,bootstyle="secondary",text="save_to_file", command=save_to_file)
button_save_to_file.pack(fill="x", padx = 20,pady = 5)




update_tool_button_colors()


root.bind("<Key>",fn_key_pressed)
root.update()



class new_tab_with_canvas:
    def __init__(self,amount_rows=60,amount_columns=60,sq_size=15,tabindex=None,matrix=None):
        # VARIABLES:
        self.amount_rows=amount_rows   #59
        self.amount_columns=amount_columns  #65
        self.sq_size = sq_size
        self.row = 0
        self.column = 0

        self.selection_vals = {

        "is_there_a_selection": False,
        "xstart":0,
        "ystart":0,
        "xend":0,
        "yend":0,
        "square_id":None
        }

        self.tabindex = tabindex

        self.mouse_position = StringVar()

        #backup_manager = class_backup_manager()


        if matrix == None:
            self.matrix = create_matrix(self.amount_rows,self.amount_columns)
        else:
            self.matrix = matrix
            self.amount_rows = len(self.matrix)
            self.amount_columns = len(self.matrix[0])


        
        #CREATE USER INTERFACE
        self.create_canvas()



    def create_canvas(self):
        self.tabFrame = Frame(tabControl)

        if self.tabindex != None:
            tabControl.insert(self.tabindex, self.tabFrame, text ='New Canvas')
        else:
            tabControl.add(self.tabFrame, text ='New Canvas')

        self.canvas_frame =  Frame(self.tabFrame)
        self.canvas_frame.pack(fill=BOTH,expand=1,padx=20,pady=20)

        self.canvas=ttk.Canvas(self.canvas_frame,bg='#000000',width=1000, height=1000,cursor="crosshair")
        self.canvas.pack(expand=1)



        self.mouse_position.set('x:?   y:?')
        self.lbl_mouse_position = Label(self.tabFrame,textvariable=self.mouse_position)
        self.lbl_mouse_position.pack(side=TOP)



        if darkdetect.theme() == "Dark":
            bg_colors = canvas_bg_dark_colors
        else:
            bg_colors = canvas_bg_light_colors


        #Create the canvas for drawing 
        x = 0
        y = 0
        even_sq = 0
        for f in range(self.amount_rows):
            x = -self.sq_size
            for c in range(self.amount_columns):
                x += self.sq_size
                even_sq = not even_sq

                if self.amount_columns % 2 == 0:
                    if f % 2 == 0:
                        if even_sq:
                            button_number = self.canvas.create_rectangle(x, y, x+self.sq_size-1,y+self.sq_size-1, fill=bg_colors[1], outline = bg_colors[1])
                        else:
                            button_number = self.canvas.create_rectangle(x, y, x+self.sq_size-1,y+self.sq_size-1, fill=bg_colors[0], outline = bg_colors[0])
                    else:
                        if even_sq:
                            button_number = self.canvas.create_rectangle(x, y, x+self.sq_size-1,y+self.sq_size-1, fill=bg_colors[0], outline = bg_colors[0])
                        else:
                            button_number = self.canvas.create_rectangle(x, y, x+self.sq_size-1,y+self.sq_size-1, fill=bg_colors[1], outline = bg_colors[1])
                else:
                    if even_sq:
                        button_number = self.canvas.create_rectangle(x, y, x+self.sq_size-1,y+self.sq_size-1, fill=bg_colors[0], outline = bg_colors[0])
                    else:
                        button_number = self.canvas.create_rectangle(x, y, x+self.sq_size-1,y+self.sq_size-1, fill=bg_colors[1], outline = bg_colors[1])
            y += self.sq_size


        self.update_canvas(self.matrix)





        #self.backup_manager.create_backup()

        #Events
        self.canvas.bind("<Button-1>", self.click_on_canvas)
        self.canvas.bind("<B1-Motion>", self.motion_click_on_canvas)
        self.canvas.bind("<Button-3>", self.right_click_on_canvas)
        self.canvas.bind("<B3-Motion>", self.motion_right_click_on_canvas)
        self.canvas.bind("<Motion>",self.update_mouse_position)
        self.canvas.bind("<Button-2>",self.fill_canvas_with_color)



        root.update()



    
    def get_hex_color_of_square(self,r,c,rgba):
        #determine the color of the square taking into account the default color of the square, 
        #the color to apply and the alpha. (returns a hex value)
        
        button_number = (r -1)*self.amount_columns + c

        if darkdetect.theme() == "Dark":
            bg_colors = canvas_bg_dark_colors
        else:
            bg_colors = canvas_bg_light_colors

        if self.amount_columns % 2 == 0:
            if r % 2 == 0:
                if button_number % 2 == 0:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( rgba[0:3] ,hex_to_rgb(bg_colors[1]), rgba[3] ) )
                else:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( rgba[0:3] ,hex_to_rgb(bg_colors[0]), rgba[3] ) )

            else:
                if button_number % 2 == 0:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( rgba[0:3] ,hex_to_rgb(bg_colors[0]), rgba[3] ) )
                else:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( rgba[0:3] ,hex_to_rgb(bg_colors[1]), rgba[3] ) )
        else:
            if button_number % 2 == 0:
                aux_hex_color = rgb_to_hex(  calculate_alpha_color( rgba[0:3] ,hex_to_rgb(bg_colors[0]), rgba[3] ) )
            else:
                aux_hex_color = rgb_to_hex(  calculate_alpha_color( rgba[0:3] ,hex_to_rgb(bg_colors[1]), rgba[3] ) )

        return aux_hex_color





    def draw_pixel(self,row,column,COLOR=None):
        if COLOR == None:
            COLOR = CURRENT_COLOR

        if row <= self.amount_rows and row >0 and column <= self.amount_columns and column >0: 
            if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$',COLOR.toHex()) and len(COLOR.toHex()) == 7:
                # n = (r-1)20 + c
                button_number = (row -1)*self.amount_columns + column

                if self.selection_vals["is_there_a_selection"]:

                    c1 = math.ceil(self.selection_vals["xstart"]/self.sq_size)
                    r1 = math.ceil(self.selection_vals["ystart"]/self.sq_size)

                    c2 = math.ceil(self.selection_vals["xend"]/self.sq_size)
                    r2 = math.ceil(self.selection_vals["yend"]/self.sq_size)

                    if c1 > c2:
                        aux = c2
                        c2 = c1
                        c1 = aux 
                    if r1 > r2:
                        aux = r2
                        r2 = r1
                        r1 = aux 

                    #c2 -= 1
                    #r2 -= 1

                    if row > r1 and row < r2 and column > c1 and column < c2:
                        self.matrix[row-1][column-1] =  COLOR.toRgba()
                        aux_hex_color = self.get_hex_color_of_square(row,column,COLOR.toRgba())
                        self.canvas.itemconfig(button_number, fill= aux_hex_color,outline=aux_hex_color  )

                else:
                    self.matrix[row-1][column-1] =  COLOR.toRgba()
                    aux_hex_color = self.get_hex_color_of_square(row,column,COLOR.toRgba())
                    self.canvas.itemconfig(button_number, fill= aux_hex_color,outline=aux_hex_color  )
            else:
                alert("Error","please write a valid hex color.")


    def remove_pixel(self,row,column):
        if row <= self.amount_rows and row >0 and column <= self.amount_columns and column >0: 
            button_number = (row -1)*self.amount_columns + column
            aux_hex_color = self.get_hex_color_of_square(row,column,[0,0,0,0])

            if self.selection_vals["is_there_a_selection"]:

                c1 = math.ceil(self.selection_vals["xstart"]/self.sq_size)
                r1 = math.ceil(self.selection_vals["ystart"]/self.sq_size)

                c2 = math.ceil(self.selection_vals["xend"]/self.sq_size)
                r2 = math.ceil(self.selection_vals["yend"]/self.sq_size)

                if c1 > c2:
                    aux = c2
                    c2 = c1
                    c1 = aux 
                if r1 > r2:
                    aux = r2
                    r2 = r1
                    r1 = aux 
                if row > r1 and row < r2 and column > c1 and column < c2:
                    self.matrix[row-1][column-1] =  (0,0,0,0)
                    self.canvas.itemconfig(button_number, fill= aux_hex_color,outline=aux_hex_color  )

            else:
                self.matrix[row-1][column-1] =  (0,0,0,0)
                self.canvas.itemconfig(button_number, fill= aux_hex_color,outline=aux_hex_color  )




    def click_on_canvas(self,event):
        global tool_type
        #backup_manager.create_backup()

        self.update_mouse_position(event)
        if tool_type == "draw_pixel":
            self.draw_pixel(self.row,self.column)
        elif tool_type == "fill_canvas_with_color":
            self.fill_canvas_with_color()
        elif tool_type == "pick_color":
            self.pick_color()
        elif tool_type == "selection_tool":
            if self.selection_vals["is_there_a_selection"] == False:
                self.selection_vals["is_there_a_selection"] = True
                self.selection_vals["xstart"] = event.x
                self.selection_vals["ystart"] = event.y
                self.selection_vals["square_id"] = self.canvas.create_rectangle(event.x, event.y,event.x, event.y,outline="#4266ff",dash=(20,20),width=10)
            else:
                self.canvas.delete(self.selection_vals["square_id"])
                self.selection_vals["is_there_a_selection"] = False
                
      

        #tool_type="draw_pixel"
        #update_tool_button_colors()
    

    def motion_click_on_canvas(self,event):
        self.update_mouse_position(event)
        if tool_type == "draw_pixel":
            self.draw_pixel(self.row,self.column)
        elif tool_type == "selection_tool":
            if self.selection_vals["is_there_a_selection"] == True:
                self.canvas.coords(self.selection_vals["square_id"],self.selection_vals["xstart"], self.selection_vals["ystart"], event.x,event.y)
                self.selection_vals["xend"] = event.x
                self.selection_vals["yend"] = event.y





    def right_click_on_canvas(self,event):
        #backup_manager.create_backup()
        self.update_mouse_position(event)
        if tool_type == "draw_pixel":
            self.remove_pixel(self.row,self.column)
        elif tool_type == "fill_canvas_with_color": 
            aux_color = color_class(_rgba_=[0,0,0,0]) #we will use this color to remove the old color from canvas
            self.fill_canvas_with_color(COLOR=aux_color)


    def motion_right_click_on_canvas(self,event):
        self.update_mouse_position(event)
        if tool_type == "draw_pixel":
            self.remove_pixel(self.row,self.column)    
     
        
    def update_mouse_position(self,event=None):
        self.column = math.ceil(event.x/self.sq_size)
        self.row = math.ceil(event.y/self.sq_size)
        
        self.mouse_position.set(f"x:{self.column} y:{self.row}")

    def is_canvas_active(self):
        return tabControl.index('current') == self.tabindex


    def pick_color(self,event=None):
        if self.matrix[self.row-1][self.column-1][3]>0:
            CURRENT_COLOR.set(self.matrix[self.row-1][self.column-1])
            update_current_color_preview()
            scl_alpha.set(CURRENT_COLOR.get255Alpha() )
            lbl_alpha_value.config(text=CURRENT_COLOR.get255Alpha() )
            scl_red.set(CURRENT_COLOR.getRed())
            scl_green.set(CURRENT_COLOR.getGreen())
            scl_blue.set(CURRENT_COLOR.getBlue())

     

    def fill_canvas_with_color(self,event=None, COLOR=None):
        #backup_manager.create_backup()

        if COLOR == None:
            COLOR = CURRENT_COLOR
        
        if self.row <= self.amount_rows and self.row >0 and self.column <= self.amount_columns and self.column >0: 
            if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', COLOR.toHex()) and len(COLOR.toHex()) == 7:
                sqs_to_fill = []
                sqs_to_fill.append((self.row,self.column))

                old_color = self.matrix[self.row-1][self.column-1]

                if old_color == COLOR.toRgba():
                    return

                while(len(sqs_to_fill) != 0):
                    row = sqs_to_fill[0][0]
                    column = sqs_to_fill[0][1]
                    del sqs_to_fill[0]

                    if row <= self.amount_rows and row >0 and column <= self.amount_columns and column >0:
                        if not ( old_color[3]==0 and COLOR.get255Alpha() == 0):
                            if  self.matrix[row-1][column-1] == old_color or (self.matrix[row-1][column-1][3] == 0 and old_color[3] == 0)  :
                                if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', COLOR.toHex()) and len(COLOR.toHex()) == 7:
                                    #if COLOR.get255Alpha() != 0:
                                    #    self.matrix[row-1][column-1] =  COLOR.toRgba()
                                    #else:
                                    #    self.matrix[row-1][column-1] = (0,0,0,0)

                                    self.draw_pixel(row,column,COLOR=COLOR)

                                    if self.selection_vals["is_there_a_selection"]:

                                        c1 = math.ceil(self.selection_vals["xstart"]/self.sq_size)
                                        r1 = math.ceil(self.selection_vals["ystart"]/self.sq_size)

                                        c2 = math.ceil(self.selection_vals["xend"]/self.sq_size)
                                        r2 = math.ceil(self.selection_vals["yend"]/self.sq_size)

                                        if c1 > c2:
                                            aux = c2
                                            c2 = c1
                                            c1 = aux 
                                        if r1 > r2:
                                            aux = r2
                                            r2 = r1
                                            r1 = aux 

                                        if row > r1 and row < r2 and column-1 > c1 and column-1 < c2:
                                            sqs_to_fill.append((row,column-1))
                                        if row > r1 and row < r2 and column+1 > c1 and column+1 < c2:
                                            sqs_to_fill.append((row,column+1))
                                        if row -1 > r1 and row-1 < r2 and column > c1 and column < c2:
                                            sqs_to_fill.append((row-1,column))
                                        if row +1 > r1 and row+1 < r2 and column > c1 and column < c2:
                                            sqs_to_fill.append((row+1,column))

                                    else:
                                        sqs_to_fill.append((row,column-1))
                                        sqs_to_fill.append((row,column+1))
                                        sqs_to_fill.append((row-1,column))
                                        sqs_to_fill.append((row+1,column))
                                else:
                                    alert("Error","please write a valid hex color.")
            else:
                alert("Error","please write a valid hex color.")


    def create_matrix_from_2_points_in_self_matrix(self,x1,y1,x2,y2):

        x1 = math.ceil(x1/self.sq_size)
        y1 = math.ceil(y1/self.sq_size)

        x2 = math.ceil(x2/self.sq_size)
        y2 = math.ceil(y2/self.sq_size)

        if x1 > x2:
            aux = x2
            x2 = x1
            x1 = aux 
        if y1 > y2:
            aux = y2
            y2 = y1
            y1 = aux 

        x2 -= 1
        y2 -= 1

        rows = y2 - y1
        columns = x2 - x1

        if rows < 1 or columns < 1:
            return None

        new_matrix = create_matrix(rows,columns)

        try:
            for r in range(y1,y2):
                for c in range(x1,x2):
                    new_matrix[r-y1][c-x1] = self.matrix[r][c]
        except:
            pass

        return new_matrix






    def create_png_from_matrix(self,matrix,sq_size): 
        img = pil.Image.new("RGBA", (len(matrix[1])*sq_size+2, len(matrix)*sq_size +2))
        draw = pil.ImageDraw.Draw(img)
        x = 0
        y = 0

        for f in matrix:
            x = -sq_size
            for c in f:
                x += sq_size
                if c[3] > 0:
                    draw.rectangle((x, y, x+sq_size-1, y+sq_size-1), fill=c)
            y += sq_size
        return img


    def image_preview(self):
        if self.selection_vals["is_there_a_selection"]:
            aux_matrix = self.create_matrix_from_2_points_in_self_matrix(self.selection_vals["xstart"],self.selection_vals["ystart"],self.selection_vals["xend"],self.selection_vals["yend"])
            img = self.create_png_from_matrix(aux_matrix,self.sq_size)
        else:
            img = self.create_png_from_matrix(self.matrix,self.sq_size)

        img.show()


    def export_as_png_file(self):
        #sq_size = call_size_chooser()

        if self.selection_vals["is_there_a_selection"]:
            aux_matrix = self.create_matrix_from_2_points_in_self_matrix(self.selection_vals["xstart"],self.selection_vals["ystart"],self.selection_vals["xend"],self.selection_vals["yend"])
            img = self.create_png_from_matrix(aux_matrix,self.sq_size)
        else:
            img = self.create_png_from_matrix(self.matrix,self.sq_size)
        
        file_name = call_save_as_file("Save as a png file:",".png")
        if file_name != None:
            img.save(file_name)


    def save_to_file(self):

        if self.selection_vals["is_there_a_selection"]:
            aux_matrix = self.create_matrix_from_2_points_in_self_matrix(self.selection_vals["xstart"],self.selection_vals["ystart"],self.selection_vals["xend"],self.selection_vals["yend"])
        else:
            aux_matrix = self.matrix

        file_name = call_save_as_file("Save:",".pxpf")
        if file_name != None:
            # writing matrix to a file
            with open(file_name, 'w') as file:
                file.write(str(aux_matrix))
            alert(app_name,"Saved")



    def update_canvas(self,mtx):
        button_number = 0
        for row in range(self.amount_rows):
            for column in range(self.amount_columns):
                button_number += 1

                aux_hex_color = self.get_hex_color_of_square(row,column,mtx[row][column])
                self.canvas.itemconfig(button_number, fill= aux_hex_color,outline =aux_hex_color  )  



    def show_instructions(self):
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






tab_with_canvas_list = []




def add_new_canvas(event=None):
    if tabControl.select() == tabControl.tabs()[-1]:
        index = len(tabControl.tabs())-1
        #frame = ttk.Frame(tabControl)
        tab_with_canvas_list.append(new_tab_with_canvas(tabindex=index))
        #tabControl.insert(index, frame, text="<untitled>")
        tabControl.select(index)

def add_new_canvas_and_load_from_file(event=None):
    if tabControl.select() == tabControl.tabs()[-1]:
        index = len(tabControl.tabs())-1
        matrix = read_matrix_from_file()
        if matrix != None:
            tab_with_canvas_list.append(new_tab_with_canvas(tabindex=index,matrix=matrix))
            tabControl.select(index)



tabControl = ttk.Notebook(root)
tabControl.pack(pady=15,padx=5,fill=X)






new_tab_menu_frame = ttk.Frame()

center_of_new_tab_menu_frame = ttk.LabelFrame(new_tab_menu_frame,text="What do you want to do?")
center_of_new_tab_menu_frame.pack(pady=50,padx=30,ipadx=100,ipady=60,expand=1)

button_add_new_canvas = ttk.Button(center_of_new_tab_menu_frame,text="Add new canvas",command=add_new_canvas)
button_add_new_canvas.pack(pady=10)

button_load_from_file = ttk.Button(center_of_new_tab_menu_frame,text="Load from file",bootstyle="secondary",command=add_new_canvas_and_load_from_file)
button_load_from_file.pack(pady=10)


tabControl.add(new_tab_menu_frame, text="┼")



start_message =f"Hi there, thanks for using PixPyinter ver: {version}, \ncurrently the project is still in development, so some features are missing."
start_message = start_message +"\n\n\nIf you are a developer and want to contribute to the project\n join: https://github.com/rc4000/PixPynter"


Label(root,text=start_message).pack()



root.bind('<Destroy>',on_window_close)
root.mainloop()




#TODO
# FIX ALERT DOEST STOP PROCESS WHEN CLOSE
