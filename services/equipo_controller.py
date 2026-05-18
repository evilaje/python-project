from models.equipo import *

def cargarEquipo(pais:str, abreviatura:str, prefijo:str, confederacion:str, grupo:str):
    cantidad = getCantidadEquiposPorGrupo(grupo)
    msj:str
    saved = False
    if (cantidad) == 4:
        msj = "Ya existen 4 equipos en este grupo"
        return (saved, msj)
        #print("Ya existen 4 equipos en este grupo")
    print(f"Cantidad de equipos en este grupo: {cantidad}")

    #validaciones hechas en los controllers/front, por eso aca na de na
    equipo:Equipo = Equipo(pais, abreviatura, prefijo, confederacion, grupo)
    if (equipo.saveEquipo()):
        msj = "Equipo Guardado Con Exito"
        saved = True
    else:
        msj = "El equipo ya existe."

    return (saved, msj)
