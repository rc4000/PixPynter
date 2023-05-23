"""
	###########################################

	here are the global variables.

	###########################################
"""



import platform
import os
import PIL as pil


OS = platform.platform().split("-")[0].lower()


if OS == 'windows':
    import ctypes as ct
else:
	pass


run = True
app_name = 'PixPynter'


version = "0.7.1-alpha"


home = os.path.expanduser("~")  #file_path a Home

runtime_path = f"{os.path.dirname(os.path.realpath(__file__))}/appdata" #file_path en donde se descomprime y ejecuta 
app_folder_path = f"{home}/.{app_name}-config"                            #file_path en donde se guarda las cosas de la app (en la carpeta del usuario)
