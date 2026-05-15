# esto se puede ampliar para guardar el minuto del gol y eso
# o que jugador metio pero idk
from utils.files_utils import *
import models.equipo as equipo

PATH = get_path("data", "partidos.json")
class Partido:
    def __init__(self, date, hora, lugar):
        self.id = self.obtenerId()
        self.fecha = date
        self.hora = hora
        self.lugar = lugar
        self.idEquipo1 = None
        self.idEquipo2 = None
        self.golesT1 = 0
        self.golesT2 = 0
        self.penalesT1 = 0
        self.penalesT2 = 0

    def toDict(self):
         return {
              "id" : self.id,
              "fecha" : self.fecha,
              "hora" : self.hora,
              "lugar" : self.lugar,
              "idEquipo1" : self.idEquipo1,
              "idEquipo2" : self.idEquipo2,
              "golesT1" : self.golesT1,
              "golesT2" : self.golesT2,
              "penalesT1" : self.penalesT1,
              "penalesT2" : self.penalesT2
         }

    """
        agregar validaciones
        -> 1 equipo no puede jugar 2 partidos el mismo dia
        -> el partido tiene que estar en rango del torneo
        -> no pueden haber 2 partidos en el mismo lugar a la misma hora
        -> equipo 1 y equipo 2 no pueden ser el mismo (igual esto se puede validar en la UI)
    """
    #las verificaciones deben ir por santos cojones en el servicio, aca se hace un quilombo
    def savePartido(self, filename=None):
        if filename is None:
            filename = PATH

        #obtener todo para volver a cargar despues, asi evitamos separar logicas de creacion de archivos (igual es re macanada pero x)
        partidos = []

        if file_exists(filename):
            with open(filename, "r") as file:
                if not is_file_empty(filename):
                    partidos = json.load(file)

        partidos.append(self.toDict())
        with open(filename, "w") as file:
            json.dump(partidos, file, indent=4)

        # aumentar los puntos de los equipos segun el resultado
        equipos = []
        with open(get_path("data", "equipos.json"), "r") as file:
            if not is_file_empty(get_path("data", "equipos.json")):
                equipos = json.load(file)

        if (len(equipos) != 0):
            for eq in equipos:
                if self.golesT1 > self.golesT2:
                    if eq["id"] == self.idEquipo1:
                        eq["puntos"] += 3
                    if eq["id"] == self.idEquipo2:
                        eq["puntos"] += 0
                elif self.golesT2 > self.golesT1:
                    if eq["id"] == self.idEquipo2:
                        eq["puntos"] += 3
                    if eq["id"] == self.idEquipo1:
                        eq["puntos"] += 0

                    # che cuando pio hay penales yo no se
                    # dudoso de esta parte del code
                else:
                    if eq["id"] == self.idEquipo1:
                        eq["puntos"] += 1
                    if eq["id"] == self.idEquipo2:
                        eq["puntos"] += 1

            with open(get_path("data", "equipos.json"), "w") as file:
                json.dump(equipos, file, indent=4)


    # esto es para el autoincrement
    def obtenerId(self, filename=None):
        if (filename is None):
            filename = PATH

        if not file_exists(filename): #por si el archivo todavia no se creo
            return 1

        with open(filename, "r") as file:
            if not is_file_empty(filename):
                partidos = json.load(file) #json load carga el contenido del archivo a la variable, en este caso como vector
                return len(partidos) + 1 if len(partidos) != 0 else 1
        return 1
    
    # esto tengo pensado mas que nada para las eliminatorias
    # porque hay que dejar los placeholders y despues meterle la data
    def setPartidoEquipos(self, idT1, idT2, filename:str = None):
        if (filename is None):
            filename = PATH

        if (file_exists(filename)):
            with open(filename, "r") as file:
                arr = json.load(file)
                for reg in arr:
                    if self.id == reg["id"]:
                        self.idEquipo1 = idT1
                        self.idEquipo2 = idT2
                        reg["idEquipo1"] = self.idEquipo1
                        reg["idEquipo2"] = self.idEquipo2

            with open(filename, "w") as file:
                json.dump(arr, file, indent=4)
        
        return None


    # al abrir la app se cargar todo en un arreglo
    def getAllPartidos(filename:str = None):
        if (filename is None):
            filename = PATH
        arr = []
        if (file_exists(filename)):
            with open(filename, "r") as file:
                if not is_file_empty(filename):
                    arr = json.load(file)
                    return arr if len(arr) > 0 else None
        return None
    
    # a partir del partido 73 ya deberia ser todo puesto automaticamente
    # tipo ganador de grupo x vs ganador de grupo y
    def setPostGrupos(self, filename:str = None):
        if (filename is None):
            filename = PATH
        partidos = []
        
        pass
    

def getPartido(id, filename:str = None):
    if (filename is None):
        filename = PATH
    arr = []
    if (file_exists(filename)):
        with open(filename, "r") as file:
            if not is_file_empty(filename):
                arr = json.load(file)
    for obj in arr:
        if (id == obj["id"]): return obj
    return None

# una jornada es una semana -> 2 partidos por grupo
# 24 partidos por jornada
# vamos a suponer que esta validado en el front que solo pueden haber 24 partidos por jornada
# porque no pienso hacer aca eso

def setEquiposFaseGrupos(filename:str = None):
    # esto es basicamente el SELECT * FROM equipos pero con pasos extra
    if (filename is None):
        filename = PATH

    # esto tiene todos los registros de equipos en forma de diccionario
    # arreglo de diccionarios
    equipos = equipo.Equipo.getAllEquipos()
    if equipos is None:
        return None
    # fin del select

    # esta parte crea un diccionario que es tipo
    # "A": [equipo1, equipo2, equipo3, equipo4], "B": [equipo5, ...]
    # lo valores del arreglo son del tipo Equipo
    # eso es para asignar los id de los equipos
    grupos = {}
    for eq in equipos:
        grupos.setdefault(eq["grupo"], []).append(eq)

    # esto en teoria itera sobre la key del diccionario
    # es para ordenar por id el array que esta como value
    for grupo in grupos:
        grupos[grupo].sort(key=lambda x: x["id"])

    # esto es basicamente el como se pueden enfrentar los equipos por grupo
    # el index 0 contra el 1 (equipo1 vs equipo2) y asi
    fixture = [
        (0, 1),
        (2, 3),
        (0, 2),
        (1, 3),
        (0, 3),
        (1, 2)
    ]

    if (file_exists(filename)):
        with open(filename, "r") as file:
            if not is_file_empty(filename):
                partidos = json.load(file)

                partido_index = 0
                grupos_ordenados = sorted(grupos.keys())

                for local1, local2 in fixture:
                    for grupo in grupos_ordenados:
                        # verificar que existan 4 equipos
                        if len(grupos[grupo]) != 4:
                            continue

                        # verificar que existan suficientes partidos para cargar
                        if partido_index >= len(partidos) or partido_index >= 72:
                            break

                        
                        partidos[partido_index]["idEquipo1"] = grupos[grupo][local1]["id"]
                        partidos[partido_index]["idEquipo2"] = grupos[grupo][local2]["id"]
                        partido_index += 1

                    if partido_index >= 72 or partido_index >= len(partidos):
                        break
        
        # guardar cambios
        with open(filename, "w") as file:
            json.dump(partidos, file, indent=4)

    return None

# en teoria ya tienen que estar cargados los horarios pero con las ID como None
# esto es casi hardcoded por el mierdon de reglamento de fifa
"""esto se puede cambiar todavia"""
def setEliminatorias(filename:str = None):
    if (filename is None):
        filename = PATH

    equipos = equipo.Equipo.getAllEquipos()
    if equipos is None:
        return None

    # esta parte crea un diccionario que es tipo -> mismo que en la funcion anterior, pego todo nomas
    # "A": [equipo1, equipo2, equipo3, equipo4], "B": [equipo5, ...]
    # lo valores del arreglo son del tipo Equipo
    # eso es para asignar los id de los equipos
    grupos = {}
    for eq in equipos:
        if eq.get("fase") != "eliminatorias":
            continue
        grupos.setdefault(eq["grupo"], []).append(eq)

    # ordeno por puntos, si tienen los mismo puntos se ordena por id
    for grupo in grupos:
        grupos[grupo].sort(key=lambda x: (x["puntos"], x["id"]), reverse=True)

    # separo por puesto
    # algunos grupos solo llevan 2 clasificados y otros llevan 3 entonces son 2 if separados
    # para que no explote todo
    ganadores = []
    subcampeones = []
    terceros = []
    for grupo in sorted(grupos.keys()):
        if len(grupos[grupo]) >= 2:
            ganadores.append(grupos[grupo][0])
            subcampeones.append(grupos[grupo][1])
            if len(grupos[grupo]) >= 3:
                terceros.append(grupos[grupo][2])

    # ordenar_terceros es la funcion custom que ordena siguiendo las reglas de fokin fifa
    mejores_terceros = equipo.ordenar_terceros(terceros)[:8]

    # bueno aca inicializo una lista vacia de partidos, una de partidos para almacenar
    # una que copia la de ganadores para hacerle pop a los que ya uso y lo mismo para los 
    # subcampeones same shiet
    matches = []
    available_ganadores = ganadores.copy()
    available_subcampeones = subcampeones.copy()


    
    for terc in mejores_terceros:
        # esto es basicamente emparejar a un tercer puesto contra un puesto 1 random
        # al parecer un puesto 3 siempre se enfrenta a un puesto 1, y como un puesto 1 no puede
        # enfrentarse a otro puesto 1 segun el reglamento entonces vamos recortando
        rival = next((g for g in available_ganadores if g["grupo"] != terc["grupo"]), None)

        # esto es una validacion bullshit por que si no hay rival entonces no hay append y
        # al final va a retornar None pero mi cerebro esta frito y no pienso hacer esto mas eficiente ahora
        if rival is None:
            continue
        # agregas el conjunto de id y removes el puesto 1 que ya se uso
        matches.append((rival["id"], terc["id"]))
        available_ganadores.remove(rival)

    #esto es lo mismo que el otro basicamente
    # con la diferencia de que aca vamos a vaciar ya los ganadores y evitamos puesto 1 vs puesto 1
    for gan in available_ganadores.copy():
        rival = next((s for s in available_subcampeones if s["grupo"] != gan["grupo"]), None)
        if rival is None:
            continue
        matches.append((gan["id"], rival["id"]))
        available_ganadores.remove(gan)
        available_subcampeones.remove(rival)

    # recorrer todos los que quedan en subChamps
    while len(available_subcampeones) >= 2:
        # salvas el dato mientras le popeas de la lista
        first = available_subcampeones.pop(0)
        second_index = next((i for i, s in enumerate(available_subcampeones) if s["grupo"] != first["grupo"]), None)
        if second_index is None:
            break
        second = available_subcampeones.pop(second_index)
        matches.append((first["id"], second["id"]))

    # si no son 16 partidos medio que algo salio mal entonces return none
    if len(matches) != 16:
        return None

    # cargamos todos los partidos que hay en el json
    partidos = []
    if file_exists(filename):
        with open(filename, "r") as file:
            if not is_file_empty(filename):
                partidos = json.load(file)

    # enumerate devuelve una matriz que es tipo (contador, value) pero itera solo como value
    # index es como le llamas a la variable, y como matches ya era luego una matriz id1 e id2 son
    # los valores i[0] e i[1]
    for index, (id1, id2) in enumerate(matches, start=72):
        partidos[index]["idEquipo1"] = id1
        partidos[index]["idEquipo2"] = id2

    # guardar todo y off al fin
    with open(filename, "w") as file:
        json.dump(partidos, file, indent=4)

    return None