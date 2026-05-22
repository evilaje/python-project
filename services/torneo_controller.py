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

def isTorneoActivo():
	if torneoExits():
		t:dict = getTorneo(1)
		return t["estaActivo"]
	return False
