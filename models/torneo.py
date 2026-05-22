from utils.files_utils import *
import models.equipo as equipo
import models.partido as partido

PATH = get_path("data", "torneos.json")

class Torneo:
	def __init__ (self, nombre: str, inicio:str, fin:str):
		self.id = self.obtenerId()
		self.nombre = nombre
		self.inicio = inicio #DD/MM/AAAA
		self.fin = fin #DD/MM/AAAA
		self.estaActivo = False # siempre false al crearse, cuando se cumplan los requisitos cambia a true
		# los requisitos serian que los grupos esten cargados totalmente y las fechas de los partidos tambien
		self.fase = "Fase de Grupos"

	def toDict(self):
		return {
			"id" : self.id,
			"nombre" : self.nombre,
			"inicio" : self.inicio,
			"fin" : self.fin,
			"estaActivo" : self.estaActivo,
			"fase" : getattr(self, "fase", "Fase de Grupos")
		}

	# validaciones en la UI
	def saveTorneo(self, filename=None):
		if (filename is None):
			filename = PATH

		torneos = []
		if (file_exists(filename)):
			with open(filename, "r") as file:
				if not is_file_empty(filename):
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
			if not is_file_empty(filename):
				torneos = json.load(file)
				return len(torneos) + 1 if len(torneos) != 0 else 1
			else:
				return 1

	# al abrir la app se cargar todo en un arreglo
	def getAllTorneos(filename:str = None):
		if (filename is None):
			filename = PATH
		arr = []
		if (file_exists(filename)):
			with open(filename, "r") as file:
				if not is_file_empty(filename):
					arr = json.load(file)
					return arr if len(arr) > 0 else None
		return None

def getTorneo(id, filename:str = None):
	if (filename is None):
		filename = PATH
	arr = []
	if (file_exists(filename)):
		with open(filename, "r") as file:
			if not is_file_empty(filename):
				arr = json.load(file)
	for obj in arr:
		if (id == obj["id"]): return obj
	return None


def avanzarFase(filename:str = None):
	if (filename is None):
		filename = equipo.PATH
	if (file_exists(filename)):
		with open(filename, "r") as file:
			if not is_file_empty(filename):
				arr = json.load(file)

				mejoresEquipos = equipo.getMejoresEquiposGrupo(filename)
				for eq in arr:
					for mejorEq in mejoresEquipos:
						if eq["id"] == mejorEq["id"]:
							eq["fase"] = "eliminatorias"
							eq["posicion"] = mejorEq["posicion"]
							break
				with open(filename, "w") as file:
					json.dump(arr, file, indent=4)

	# actualizar la fase del torneo en el archivo de torneos
	if file_exists(PATH):
		with open(PATH, "r") as tf:
			if not is_file_empty(PATH):
				torneos = json.load(tf)
				if torneos and len(torneos) > 0:
					# se asume un único torneo activo; actualizar el primero
					torneos[0]["fase"] = "16avos de Final"
					with open(PATH, "w") as tfw:
						json.dump(torneos, tfw, indent=4)


def setFaseTorneo(fase:str, filename:str = None):
	if (filename is None):
		filename = PATH
	if not file_exists(filename):
		return False
	with open(filename, "r") as file:
		if is_file_empty(filename):
			return False
		torneos = json.load(file)
	if not torneos:
		return False
	torneos[0]["fase"] = fase
	with open(filename, "w") as file:
		json.dump(torneos, file, indent=4)
	return True

#preguntar si existe un torneo (literal si existe UNA unidad de torneo)
def torneoExits()-> bool:
	if file_exists(PATH):
		with open(PATH, "r") as file:
			return True if not is_file_empty(PATH) else False
	return False
