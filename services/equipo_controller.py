from models.equipo import *

def cargarEquipo(pais:str, abreviatura:str, prefijo:str, confederacion:str):
    cantidad = getCantidadAllEquipos()
    msj:str
    saved = False
    if (cantidad) == 48:
        msj = "Ya existen 48 equipos participantes"
        return (saved, msj)
        #print("Ya existen 4 equipos en este grupo")
    print(f"Cantidad de equipos: {cantidad}")

    #validaciones hechas en los controllers/front, por eso aca na de na
    equipo:Equipo = Equipo(pais, abreviatura, prefijo, confederacion)
    if (equipo.saveEquipo()):
        msj = "Equipo Guardado Con Exito"
        saved = True
    else:
        msj = "El equipo ya existe."

    return (saved, msj)

#la funcion para la vista 3 de configHandler
def cargarGrupo(pais: str, grupo: str):
    cantidad = getCantidadEquiposPorGrupo(grupo)
    msj:str
    saved = False
    if (cantidad) == 4:
        msj = "Este grupo ya esta completo"
        return (saved, msj)
        #print("Ya existen 4 equipos en este grupo")
        
    else:
        setGrupo(pais, grupo)


def getEquiposPorGrupo(grupo: str, filename=PATH):
    equipos = Equipo.getAllEquipos(filename)
    if not equipos:
        return []
    return [e for e in equipos if e.get("grupo", "") == grupo]


def validarGrupo(paises):
    if len(paises) != 4 or any(not pais.strip() for pais in paises):
        return False, "Se deben llenar los campos"
    if len(set(paises)) != len(paises):
        return False, "No se pueden repetir paises"
    return True, None


def guardarGrupo(grupo: str, paises: list):
    valid, mensaje = validarGrupo(paises)
    if not valid:
        return False, mensaje, []

    if not grupo:
        return False, "Se deben llenar los campos", []

    grupo_equipos = getEquiposPorGrupo(grupo)
    if len(grupo_equipos) == 4:
        return False, "El grupo ya está cargado", [e["pais"] for e in grupo_equipos]

    for pais in paises:
        cargarGrupo(pais, grupo)

    return True, "Grupo guardado correctamente", None

