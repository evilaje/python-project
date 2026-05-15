from utils.files_utils import *
import utils.json_utils as json_utils
# path tiene la ruta del json donde se guardan los equipos
# pero no es la ruta completa, es la variable archivo que se pasa a get_path en files_utils
PATH = get_path("data", "equipos.json")
class Equipo:
    def __init__(self, pais, abv, prefix, conf, grupo, puntos = 0):
        self.id = None # depende del grupo y el orden de carga
        self.pais = pais.capitalize()
        self.abreviatura = abv
        self.prefijo = prefix
        self.confederacion = conf
        self.grupo = grupo
        self.puntos = puntos
        self.fase = "grupos"
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
            with open(filename, "r") as file:
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
            with open(filename, "r") as file:
                if not is_file_empty(filename): #verifica que el archivo no este vacio
                    # tbs es para cargar un arreglo con los diccionarios que estan en el json
                    equipos = json.load(file)

        # i = len(equipos) + 1
        # bucle para evitar equipos repetidos
        # compara todos los equipos existentes en el json con self y existe uno con la misma id, return/exit
        if len(equipos) != 0: #no hace falta buscar nada si no hay nada
            for eq in equipos:
                if (eq["id"] == self.id or eq["prefijo"] == self.prefijo):
                    print("No se guardara el equipo")
                    return

        equipos.append(self.toDict())
        json_utils.sort_json(equipos)


        # guarda el diccionario equipos en la direccion de file, con indentacion de 4 espacios (1 tab)
        with open(filename, "w") as file:
            json.dump(equipos, file, indent=4)

    # esto es para el autoincrement
    def obtenerId(self, filename=None):
        if (filename is None):
            filename = PATH

        if not file_exists(filename): #por si el archivo todavia no se creo
            return 1

        with open(filename, "r") as file:
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
            with open(filename, "r") as file:
                if not is_file_empty(filename):
                    arr = json.load(file)
                    return arr if len(arr) > 0 else None
        return None #importante verificar siempre el None            


# obtiene los goles de x equipo
def getGoles(id, filename:str = get_path("data", "partidos.json")):

    if not file_exists(filename):
        return 1

    with open(filename, "r") as file:
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

    with open(filename, "r") as file:
        if not is_file_empty(filename):
            partidos = json.load(file)
            mejorDiferencia = None
            golesFavor = 0
            golesContra = 0
            for p in partidos:
                if p["idEquipo1"] == id:
                    golesFavor = p["golesT1"]
                    golesContra = p["golesT2"]
                elif p["idEquipo2"] == id:
                    golesFavor = p["golesT2"]
                    golesContra = p["golesT1"]

                if mejorDiferencia is None or golesFavor - golesContra > mejorDiferencia:
                    mejorDiferencia = golesFavor - golesContra

            return mejorDiferencia
        return None

# ngl este yo estaba viendo la comparacion de los mejores terceros y copilot se altero y me dijo
# escribi esto y yo le hice caso, voy a comentar lo que entiendo igual
def ordenar_terceros(terceros):
    # definir la funcion aca adentro es tipo hacer private funcion porque total no se usa en ningun otro lado xd
    def key_eq(eq):
        diferencia = getDiferenciaGoles(eq["id"])
        goles = getGoles(eq["id"])
        return (
            eq.get("puntos", 0),
            diferencia if diferencia is not None else -9999,
            goles if goles is not None else -9999,
            eq.get("prefijo", "")
        )
    # ok al parecer key=key_eq lo que hace es alterar el funcionamiento del sort
    # le dice que ordene primero por puntos, despues por la mayor diferencia de goles en un partido
    # (esa funcion hice esta en algun lado), despues goles totales (tambien otra funcion) y de ultimo compara los prefix
    return sorted(terceros, key=key_eq, reverse=True)

"""verificar validaciones despues"""
# esta funcion retorna la id del equipo que quedo puesto pos en el grupo que se le mande
# eso en teoria no se no probe me dio paja
def getPosicionGrupo(pos, grupo, filename:str = None):
    if (filename is None):
        filename = PATH
    arr = []
    if (file_exists(filename)):
        with open(filename, "r") as file:
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
        with open(filename, "r") as file:
            if not is_file_empty(filename):
                arr = json.load(file)
            else: #si el archivo esta vacio no obtenemos nada
                return None
    for obj in arr:
        if (id == obj["id"]): return obj
    return None

# funcion de mierda para conseguir los equipo que pasan la puta fase de grupos
# que muchas validaciones mierdon
"""no se ni si funciona esto, verificar"""
def getMejoresEquiposGrupo(filename:str = None):
    if (filename is None):
        filename = PATH
    arr = []
    if (file_exists(filename)):
        with open(filename, "r") as file:
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
                    equiposGrupo.sort(key=lambda x: x["puntos"], reverse=True) 
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