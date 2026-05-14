from utils.files_utils import *

PATH = get_path("data", "torneos.json")

class Torneo:
	def __init__ (self, nombre: str, inicio:str, fin:str):
		self.id = self.obtenerId()
		self.nombre = nombre
		self.inicio = inicio #DD/MM/AAAA
		self.fin = fin #DD/MM/AAAA
		self.estaActivo = False # siempre false al crearse, cuando se cumplan los requisitos cambia a true
		# los requisitos serian que los grupos esten cargados totalmente y las fechas de los partidos tambien
	
	def toDict(self):
		return {
			"id" : self.id,
			"nombre" : self.nombre,
			"inicio" : self.inicio,
			"fin" : self.fin,
			"estaActivo" : self.estaActivo
		}

	# validaciones en la UI
	def saveTorneo(self, filename=None):
		if (filename is None):
			filename = PATH

		torneos = []
		if (file_exists(filename)):
			with open(filename, "r") as file:
				torneos = json.load(file)

		# mirar si ya existe el nombre que se metio en el archivo, es que el id es autoincremental xd
		#a lo mejor hay que echarle un ojo a esta valiacion
		for t in torneos:
			if (self.nombre == t["nombre"]):
				print("ya existe el torneo, no se guardara.")
				return

		torneos.append(self.toDict())

		with open(filename, "w") as file:
			json.dump(torneos, file, indent=4)

	#tdv no hice nada con esto xd, solo evitar 	q se modifique si el torneo ya emppezo
	def editTorneo(self, inicio:str, fin:str):
		if (not self.estaActivo):
			pass
		# tengo pensado que no se pueden cambiar los nombres de los torneos, solo las fechas
		self.inicio = inicio
		self.fin = fin
		
		# como no hay mas de un torneo entonces guardar nomas nb
		self.saveTorneo()

	# bs para el autoincrement
	def obtenerId(self, filename=None):
		if filename is None:
			filename = PATH

		if not file_exists(filename):
			return 1

		with open(filename, "r") as file:
			torneos = json.load(file)
			return len(torneos) + 1 if len(torneos) != 0 else 1

	# al abrir la app se cargar todo en un arreglo
	def getAllTorneos(filename:str = None):
		if (filename is None):
			filename = PATH
		arr = []
		if (file_exists(filename)):
			with open(filename, "r") as file:
				arr = json.load(file)
				return arr if len(arr) > 0 else None
		return None

def getTorneo(id, filename:str = None):
	if (filename is None):
		filename = PATH
	arr = []
	if (file_exists(filename)):
		with open(filename, "r") as file:
			arr = json.load(file)
	for obj in arr:
		if (id == obj["id"]): return obj
	return None
