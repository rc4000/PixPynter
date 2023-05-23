from gui import *
from ast import literal_eval


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
    def __init__(self,_rgba_=[255,255,255,255]):
        self._rgba_ = _rgba_
        
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
    



def create_matrix(amount_rows,amount_columns):
    matrix = []
    for f in range(amount_rows):
        matrix = matrix + [[]]

    for c in matrix:
        for f in range(amount_columns):
            c.append((0,0,0,0))
    return matrix



def read_matrix_from_file():
    file_name = call_file_chooser(".pxpf")
    if file_name != None:
        with open(file_name,"r") as file:
            new_matrix = literal_eval(file.read())
        return new_matrix
    else:
        return None






class class_backup_manager:
    def __init__(self):
        self.backups = []
        self.backup_current_index = -1
    def create_backup(self):
        print("BUCKUP ")
        print(f"backup_current_index: {self.backup_current_index}  backups: {len(self.backups)}")
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
    def load_backup_to_canvas(self,event=None):
        #print(self.backup_current_index)
        mtx = self.backups[self.backup_current_index]
        print("LOADED ")
        print(f"backup_current_index: {self.backup_current_index}  backups: {len(self.backups)}")

        global matrix; matrix = mtx

        if self.backup_current_index > 0:
            del self.backups[self.backup_current_index]

        if self.backup_current_index > 0:
            self.backup_current_index -= 1 
        button_number = 0
        for row in range(amount_rows):
            for column in range(amount_columns):
                button_number += 1

                if not button_number % 2 == 0:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( mtx[row][column][0:3] ,hex_to_rgb("#222222"),mtx[row][column][3]))
                else:
                    aux_hex_color = rgb_to_hex(  calculate_alpha_color( mtx[row][column][0:3] ,hex_to_rgb("#333333"),mtx[row][column][3]))

                canvas.itemconfig(button_number, fill= aux_hex_color,outline =aux_hex_color  )
      

