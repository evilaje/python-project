from clases.torneo import *
#funciones pensadas para q las llamen botones o cosas por ahi, asi no mezclamos la logica de la interfaz con la logica de las entidades
def cargarTorneo(nombre:str, inicio:str, fin:str):
	#validaciones de fechas hechas en los controllers/front, por eso aca na de na
	torneo:Torneo = Torneo(nombre, inicio, fin)
	torneo.saveTorneo()

def buscarTorneo(nombre:str):
	return selectTorneo(nombre)
