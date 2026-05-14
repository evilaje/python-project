from utils.files_utils import *


PATH = get_path("data", "equipos.json")
class Equipo:
    def __init__(self, id, pais, abv, prefix, conf, grupo):
        self.id = id
        self.pais = pais
        self.abreviatura = abv
        self.prefijo = prefix
        self.confederacion = conf
        self.grupo = grupo

        # self.saveEquipo()
    def toDict(self):
        return {
            "id" : self.id,
            "pais" : self.pais,
            "abreviatura" : self.abreviatura,
            "prefijo" : self.prefijo,
            "confederacion" : self.confederacion,
            "grupo" : self.grupo
        }


    # bs para guardar la data en un archivo
    # podemos usar el identificador para encontrar el lugar
    def saveEquipo(self, filename=None):
        if (filename is None):
            filename = PATH

        equipos = []
        if file_exists(filename):
            with open(filename, "r") as file:
                equipos = json.load(file)

        for eq in equipos:
            if (self.id == eq["id"]):
                print("el equipo ya existe, no se va a guardar")
                return

        equipos.append(self.toDict())

        with open(filename, "w") as file:
            json.dump(equipos, file, indent=4)

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
