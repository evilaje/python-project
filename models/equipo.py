from utils.files_utils import *

# path tiene la ruta del json donde se guardan los equipos
# pero no es la ruta completa, es la variable archivo que se pasa a get_path en files_utils
PATH = get_path("data", "equipos.json")
class Equipo:
    def __init__(self, pais, abv, prefix, conf, grupo, puntos = 0):
        self.id = None # depende del grupo y el orden de carga
        self.abreviatura = abv
        self.prefijo = prefix
        self.confederacion = conf
        self.grupo = grupo
        self.puntos = puntos

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
            "puntos" : self.puntos
        }


    def setId(self, filename:str = None):
        if (filename is None):
            filename = PATH

        equipos = []
        if file_exists(filename):
            with open(filename, "r") as file:
                equipos = json.load(file)

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
                # tbs es para cargar un arreglo con los diccionarios que estan en el json
                equipos = json.load(file)

        # i = len(equipos) + 1
        # bucle para evitar equipos repetidos
        # compara todos los equipos existentes en el json con self y existe uno con la misma id, return/exit
        for eq in equipos:
            if (eq["id"] == self.id):
                print("No se guardara el equipo")
                return

        equipos.append(self.toDict())
        # key = lambda eq -> esta bs define un criterio despues del :, le llama eq a cada elemento del arreglo
        # basicamente ordena primero por grupo, y en el orden por grupo hace un sort por id
        """ver para cambiar"""
        equipos.sort(key=lambda eq: (eq["grupo"], eq["id"]))

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
            equipos = json.load(file) #json load carga el contenido del archivo a la variable, en este caso como vector
            return len(equipos) + 1 if len(equipos) != 0 else 1
        
    # obtiene los goles de x equipo
    def getGoles(self, filename:str = get_path("data", "partidos.json")):
                
        if not file_exists(filename):
            return 1
        
        with open(filename, "r") as file:
            partidos = json.load(file)
            goles = 0
            for p in partidos:
                if p["equipo1"] == self.id:
                    goles += p["golesEquipo1"]
                elif p["equipo2"] == self.id:
                    goles += p["golesEquipo2"]

            return goles

    # al abrir la app se cargar todo en un arreglo
    def getAllEquipos(filename:str = None):
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
