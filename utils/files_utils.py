import json
import os

# ts funciona asi mas o menos -> __file__ devuelve la ruta del archivo actual o sea files_utils
# con os.path.dirname conseguimos la ubicacion del parent que es la carpeta utils y con el 2do dirname la de el proyecto
# es tipo la direccion del root del proyecto pero no hardcodeada
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_path(folder:str, name:str) -> str:
	# el join este concatena la direccion del proyecto con una carpeta y un archivo
	# basicamente hace lo que dice el nombre de la funcion xd
	return os.path.join(DIR_BASE, folder, name)

def file_exists(filename:str):
	# esto es para que no se ponga a tratar de trabajar en un archivo que no existe y eso
	return os.path.exists(filename)

def is_file_empty(filename:str) -> bool:
	with open(filename, "r") as file:
		var = file.read().strip()
		#print(var)
		if not var: print(f"El archivo {filename} esta vacio!" )
		return True if (not var) else False #retorna True si no hay var: esta vacio xd
