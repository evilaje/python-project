import json
from utils.files_utils import *
import utils.json_utils as json_utils
# path tiene la ruta del json donde se guardan los equipos
# pero no es la ruta completa, es la variable archivo que se pasa a get_path en files_utils
PATH = get_path("data", "equipos.json")
class Equipo:
    def __init__(self, pais, abv, prefix, conf, puntos = 0):
        self.id = None # depende del grupo y el orden de carga
        self.pais = pais.capitalize()
        self.abreviatura = abv
        self.prefijo = prefix
        self.confederacion = conf
        self.grupo = "placeholder"
        self.puntos = puntos
        # fase legible para mostrar en reportes
        self.fase = "Fase de Grupos"
        self.posicion = None # para cuando aavance de fase, tipo que diga puesto 1 o una mierda asi

        self.setId()

    # esto convierte el objeto en un diccionario para
    # que se pueda guardar en el json
    def toDict(self):
        return {
            "id" : self.id,
            "pais" : self.pais,
            "abreviatura" : self.abreviatura,
            "prefijo" : self.prefijo,
            "confederacion" : self.confederacion,
            "grupo" : self.grupo,
            "puntos" : self.puntos,
            "fase" : self.fase,
            "posicion" : self.posicion
        }


    def setId(self, filename:str = None):
        if (filename is None):
            filename = PATH

        equipos = []
        if file_exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                if not is_file_empty(filename):
                    equipos = json.load(file)
                else:
                    print("El archivo de equipos esta vacio")

        # el id depende del grupo, tipo si es el primero del grupo A entonces id = "A1", el segundo es "A2"
        # el primero del grupo B es "B1", el segundo "B2" y sigue

        # variable auxliiar para contar los equipor per grupo
        count = 1
        for eq in equipos:
            if eq["grupo"] == self.grupo:
                count += 1

        self.id = self.grupo + str(count)


    # bs para guardar la data en un archivo
    # podemos usar el identificador para encontrar el lugar
    def saveEquipo(self, filename:str = None):
        if (filename is None):
            filename = PATH
        equipos = []
        if file_exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                if not is_file_empty(filename): #verifica que el archivo no este vacio
                    # tbs es para cargar un arreglo con los diccionarios que estan en el json
                    equipos = json.load(file)

        # i = len(equipos) + 1
        # bucle para evitar equipos repetidos
        # compara todos los equipos existentes en el json con self y existe uno con la misma id, return/exit
        if len(equipos) != 0: #no hace falta buscar nada si no hay nada
            for eq in equipos:
                #como el id depende del orden de carga y el grupo no se repite nunca:
                #mejor busco pais o prefijo
                if (eq["pais"] == self.pais or eq["prefijo"] == self.prefijo):
                    print("No se guardara el equipo")
                    print(f"Equipo no guardado: {self.toDict()}")
                    print(f"Este equipo es igual: {eq}")
                    return False

        equipos.append(self.toDict())
        json_utils.sort_json(equipos)



        # guarda el diccionario equipos en la direccion de file, con indentacion de 4 espacios (1 tab)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(equipos, file, indent=4)
        return True


    # esto es para el autoincrement
    def obtenerId(self, filename=None):
        if (filename is None):
            filename = PATH

        if not file_exists(filename): #por si el archivo todavia no se creo
            return 1

        with open(filename, "r", encoding="utf-8") as file:
            if not is_file_empty(filename):
                equipos = json.load(file) #json load carga el contenido del archivo a la variable, en este caso como vector
                return len(equipos) + 1 if len(equipos) != 0 else 1
            return 1


    # al abrir la app se cargar todo en un arreglo
    def getAllEquipos(filename:str = None):
        if (filename is None):
            filename = PATH
        arr = []
        if (file_exists(filename)):
            with open(filename, "r", encoding="utf-8") as file:
                if not is_file_empty(filename):
                    arr = json.load(file)
                    return arr if len(arr) > 0 else None
        return None #importante verificar siempre el None


    def getAbreviatura(self, filename: str = None):
        if (filename is None):
            filename = PATH

        equipos = []

        if (file_exists(filename)):
            with open(filename, "r", encoding="utf-8") as file:
                equipos = json.load(file)

                for equipo in equipos:
                    if equipo["id"] == self.id:
                        return equipo["abreviatura"]

        return None



# funcion para setear grupo en la vista 3 de configHandler
def setGrupo(pais: str, grupo: str, filename = PATH):

    if not file_exists(filename):
        return 1

    equipos = []

    with open(filename, "r", encoding="utf-8") as file:
        if not is_file_empty(filename):
            equipos = json.load(file)
            for eq in equipos:
                if pais == eq["pais"]:
                    equipo = Equipo(
                        eq["pais"],
                        eq["abreviatura"],
                        eq["prefijo"],
                        eq["confederacion"],
                        eq["puntos"]
                    )

                    equipo.grupo = grupo
                    equipo.setId()
                    eq["grupo"] = grupo
                    eq["id"] = equipo.id
                    break


    with open(filename, "w", encoding="utf-8") as file:
        json.dump(equipos, file, indent=4)

    return None


# obtiene los goles de x equipo
def getGoles(id, filename:str = get_path("data", "partidos.json")):

    if not file_exists(filename):
        return 1

    with open(filename, "r", encoding="utf-8") as file:
        if not is_file_empty(filename):
            partidos = json.load(file)
            goles = 0
            for p in partidos:
                if p["idEquipo1"] == id:
                    goles += p["golesT1"]
                elif p["idEquipo2"] == id:
                    goles += p["golesT2"]

            return goles
        return None

def getDiferenciaGoles(id, filename:str = get_path("data", "partidos.json")):

    if not file_exists(filename):
        return 1

    with open(filename, "r", encoding="utf-8") as file:
        if not is_file_empty(filename):
            partidos = json.load(file)
            golesFavor = 0
            golesContra = 0
            for p in partidos:
                if p["idEquipo1"] == id:
                    golesFavor += p["golesT1"]
                    golesContra += p["golesT2"]
                elif p["idEquipo2"] == id:
                    golesFavor += p["golesT2"]
                    golesContra += p["golesT1"]

            return golesFavor - golesContra
        return None

# ngl este yo estaba viendo la comparacion de los mejores terceros y copilot se altero y me dijo
# escribi esto y yo le hice caso, voy a comentar lo que entiendo igual
def ordenar_terceros(terceros):
    return ordenar_equipos(terceros)


"""verificar validaciones despues"""
# esta funcion retorna la id del equipo que quedo puesto pos en el grupo que se le mande
# eso en teoria no se no probe me dio paja
def getPosicionGrupo(pos, grupo, filename:str = None):
    if (filename is None):
        filename = PATH
    arr = []
    if (file_exists(filename)):
        with open(filename, "r", encoding="utf-8") as file:
            if not is_file_empty(filename):
                arr = json.load(file)
                equiposGrupo = []
                for eq in arr:
                    if eq["grupo"] == grupo:
                        equiposGrupo.append(eq)
                equiposGrupo.sort(key=lambda x: x["puntos"], reverse=True)

                return equiposGrupo[pos-1]["id"] if len(equiposGrupo) >= pos else None


def getEquipo(id, filename:str = None):
    if (filename is None):
        filename = PATH
    arr = []
    if (file_exists(filename)):
        with open(filename, "r", encoding="utf-8") as file:
            if not is_file_empty(filename):
                arr = json.load(file)
            else: #si el archivo esta vacio no obtenemos nada
                return None
    for obj in arr:
        if (id == obj["id"]): return obj
    return None

def ordenar_equipos(equipos):
    """Ordena equipos con prioridad:
    1) más puntos
    2) mayor diferencia de goles
    3) más goles marcados
    Desempate final: prefijo.
    """
    def key_eq(eq):
        puntos = eq.get("puntos", 0)
        diferencia = getDiferenciaGoles(eq["id"])
        goles = getGoles(eq["id"])

        return (
            puntos,
            diferencia if diferencia is not None else -9999,
            goles if goles is not None else -9999,
            eq.get("prefijo", ""),
        )

    return sorted(equipos, key=key_eq, reverse=True)


# funcion de mierda para conseguir los equipo que pasan la puta fase de grupos
# que muchas validaciones mierdon
"""no se ni si funciona esto, verificar"""
def getMejoresEquiposGrupo(filename:str = None):
    if (filename is None):
        filename = PATH
    arr = []
    if (file_exists(filename)):
        with open(filename, "r", encoding="utf-8") as file:
            if not is_file_empty(filename):
                arr = json.load(file)
                mejoresEquipos = []
                tercerosPuestos = []

                # esto agrega los 2 mejores equipos per grupo
                for grupo in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]:
                    equiposGrupo = []
                    for eq in arr:
                        if eq["grupo"] == grupo:
                            equiposGrupo.append(eq)
                    equiposGrupo = ordenar_equipos(equiposGrupo)
                    i = 0
                    for eq in equiposGrupo:
                        eq["posicion"] = i+1
                        i += 1

                    mejoresEquipos.append(equiposGrupo[0])
                    mejoresEquipos.append(equiposGrupo[1])
                    tercerosPuestos.append(equiposGrupo[2])

                mejoresEquipos.extend(ordenar_terceros(tercerosPuestos)[:8]) #agrega los 8 mejores terceros puestos
                return mejoresEquipos

    return None

def getCantidadEquiposPorGrupo(grupo:str, filename = PATH):
    count = 0
    equipos = []
    if file_exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            if not is_file_empty(filename):
                equipos = json.load(file)
                for eq in equipos:
                    if eq["grupo"] == grupo:
                        count += 1
            else:
                return -1 #archivo vacio, no creo que se use
    return count

def getCantidadAllEquipos(filename = PATH):
    count = 0
    equipos = []
    if file_exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            if not is_file_empty(filename):
                equipos = json.load(file)
                count = len(equipos)
            else:
                return -1 #archivo vacio, no creo que se use
    return count


def recalcularPuntos(filename: str = None):
    if filename is None:
        filename = PATH

    equipos_file = get_path("data", "equipos.json")

    if not file_exists(filename) or not file_exists(equipos_file):
        return False

    with open(filename, "r", encoding="utf-8") as f:
        partidos = json.load(f)

    with open(equipos_file, "r", encoding="utf-8") as f:
        equipos = json.load(f)

    # Resetear todos los puntos a 0
    for eq in equipos:
        eq["puntos"] = 0

    # Recalcular desde todos los partidos jugados
    for partido in partidos:
        if not partido.get("jugado"):
            continue

        id_t1 = partido.get("idEquipo1")
        id_t2 = partido.get("idEquipo2")
        g1 = partido.get("golesT1", 0)
        g2 = partido.get("golesT2", 0)

        if not id_t1 or not id_t2:
            continue

        for eq in equipos:
            eq.setdefault("puntos", 0)
            if g1 > g2:
                if eq["id"] == id_t1:
                    eq["puntos"] += 3
            elif g2 > g1:
                if eq["id"] == id_t2:
                    eq["puntos"] += 3
            else:  # empate, incluyendo 0-0
                if eq["id"] == id_t1 or eq["id"] == id_t2:
                    eq["puntos"] += 1

    with open(equipos_file, "w", encoding="utf-8") as f:
        json.dump(equipos, f, indent=4)

    return True

