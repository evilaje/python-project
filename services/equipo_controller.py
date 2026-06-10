from models.equipo import *
from utils.files_utils import get_path

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


def getTablaDeGrupo(grupo: str):
    """Devuelve la tabla de posiciones para un grupo.

    Cada entrada tiene las claves esperadas por la UI:
    'posicion','pais','pj','g','e','p','gf','gc','dg','pts'
    """
    # obtener equipos del grupo
    equipos = getEquiposPorGrupo(grupo)
    if not equipos:
        return []

    # inicializar estructura por id
    tabla = {}
    for eq in equipos:
        tabla[eq["id"]] = {
            "id": eq["id"],
            "pais": eq.get("pais", ""),
            "abreviatura": eq.get("abreviatura", ""),
            "pj": 0,
            "g": 0,
            "e": 0,
            "p": 0,
            "gf": 0,
            "gc": 0,
            "dg": 0,
            "pts": 0
        }

    # leer partidos y acumular estadisticas
    partidos_file = get_path("data", "partidos.json")
    partidos = []
    from utils.files_utils import file_exists, is_file_empty
    import json
    if file_exists(partidos_file):
        with open(partidos_file, "r") as f:
            if not is_file_empty(partidos_file):
                partidos = json.load(f)

    for p in partidos:
        id1 = p.get("idEquipo1")
        id2 = p.get("idEquipo2")

        # solo nos interesan partidos donde ambos equipos pertenezcan al grupo
        # Además: considerar exclusivamente los 72 partidos de fase de grupos
        partido_id = p.get("id", 0) or 0
        if partido_id > 72:
            continue
        if id1 not in tabla and id2 not in tabla:
            continue

        # OJO: un 0-0 válido (golesT1=0 y golesT2=0) debe contar.
        # Solo ignoramos si el partido NO está marcado como jugado.
        if not p.get("jugado", False):
            continue

        g1 = p.get("golesT1", 0) or 0
        g2 = p.get("golesT2", 0) or 0
        pen1 = p.get("penalesT1", 0) or 0
        pen2 = p.get("penalesT2", 0) or 0


        # actualizar solo si el equipo participa en el grupo
        if id1 in tabla:
            tabla[id1]["pj"] += 1
            tabla[id1]["gf"] += g1
            tabla[id1]["gc"] += g2

        if id2 in tabla:
            tabla[id2]["pj"] += 1
            tabla[id2]["gf"] += g2
            tabla[id2]["gc"] += g1

        # resultado
        if id1 in tabla and id2 in tabla:
            if g1 > g2:
                tabla[id1]["g"] += 1
                tabla[id2]["p"] += 1
                tabla[id1]["pts"] += 3
            elif g2 > g1:
                tabla[id2]["g"] += 1
                tabla[id1]["p"] += 1
                tabla[id2]["pts"] += 3
            else:
                tabla[id1]["e"] += 1
                tabla[id2]["e"] += 1
                tabla[id1]["pts"] += 1
                tabla[id2]["pts"] += 1

        else:
            # si solo uno del partido pertenece al grupo (raro), no contar resultado de puntos
            # pero si queremos se puede contar solo los goles/PJ; por ahora contamos PJ y goles arriba
            pass

    # calcular diferencia de goles y transformar a lista
    resultado = []
    for idx, data in tabla.items():
        data["dg"] = data["gf"] - data["gc"]
        resultado.append({
            "posicion": 0,
            "pais": data["pais"],
            "abreviatura": data["abreviatura"],
            "pj": data["pj"],
            "g": data["g"],
            "e": data["e"],
            "p": data["p"],
            "gf": data["gf"],
            "gc": data["gc"],
            "dg": data["dg"],
            "pts": data["pts"],
            "id": data["id"]
        })

    # ordenar por puntos, luego diferencia de goles, luego gf
    resultado.sort(key=lambda x: (x.get("pts", 0), x.get("dg", 0), x.get("gf", 0)), reverse=True)

    # asignar posiciones
    for i, row in enumerate(resultado, start=1):
        row["posicion"] = i

    return resultado


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

