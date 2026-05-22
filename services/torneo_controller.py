from models.torneo import *
#funciones pensadas para q las llamen botones o cosas por ahi, asi no mezclamos la logica de la interfaz con la logica de las entidades
def cargarTorneo(nombre:str, inicio:str, fin:str):
	#validaciones de fechas hechas en los controllers/front, por eso aca na de na
	torneo:Torneo = Torneo(nombre, inicio, fin)
	torneo.saveTorneo()

def buscarTorneo(id:int):
	return getTorneo(id, PATH)

def getRangoTorneo():
	if torneoExits():
		t:dict = getTorneo(1)
		torneo_ini = t["inicio"]
		torneo_fin = t["fin"]
		return (torneo_ini, torneo_fin)
	else:
		return None

def canSkipTorneoVista():
	return torneoExits()


def activarTorneo(id:int = 1):
	if not torneoExits():
		return False

	with open(PATH, "r") as file:
		if is_file_empty(PATH):
			return False
		torneos = json.load(file)

	if not torneos:
		return False

	updated = False
	for t in torneos:
		if t.get("id") == id:
			t["estaActivo"] = True
			updated = True
			break

	if not updated:
		return False

	with open(PATH, "w") as file:
		json.dump(torneos, file, indent=4)

	return True


def isTorneoActivo():
	if torneoExits():
		t:dict = getTorneo(1)
		return t["estaActivo"]
	return False
