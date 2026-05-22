# esto se puede ampliar para guardar el minuto del gol y eso
# o que jugador metio pero idk
from utils.files_utils import *
import models.equipo as equipo

PATH = get_path("data", "partidos.json")
class Partido:
    def __init__(self, date, hora, lugar, fase: str = "Fase de Grupos"):
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
        self.fase = fase
        self.jugado = False

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
              "penalesT2" : self.penalesT2,
              "fase" : self.fase,
              "jugado" : self.jugado
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
    @staticmethod
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

    @staticmethod
    def ordenar_partidos_por_fecha_y_reasignar_ids(filename:str = None):
        if (filename is None):
            filename = PATH
        if not file_exists(filename):
            return False

        with open(filename, "r") as file:
            if is_file_empty(filename):
                return False
            partidos = json.load(file)

        from datetime import datetime
        for partido in partidos:
            fecha = partido.get("fecha", "").strip()
            hora = partido.get("hora", "").strip()
            try:
                datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")
            except Exception:
                return False

        partidos.sort(key=lambda partido: datetime.strptime(
            f"{partido.get('fecha', '').strip()} {partido.get('hora', '').strip()}",
            "%d/%m/%Y %H:%M"
        ))

        for index, partido in enumerate(partidos, start=1):
            partido["id"] = index

        with open(filename, "w") as file:
            json.dump(partidos, file, indent=4)

        return True
    
    # a partir del partido 73 ya deberia ser todo puesto automaticamente
    # tipo ganador de grupo x vs ganador de grupo y
    def setPostGrupos(self, filename:str = None):
        if (filename is None):
            filename = PATH
        partidos = []
        
        pass

    def setGoles(self, filename: str = None):
        if (filename is None):
            filename = PATH
        
        partidos = []

        if (file_exists(filename)):
            with open(filename, "r") as file:
                partidos = json.load(file)

            for partido in partidos:
                if partido["id"] == self.id:
                    # conservar goles previos para evitar doble conteo
                    prev_g1 = partido.get("golesT1", 0)
                    prev_g2 = partido.get("golesT2", 0)

                    partido["golesT1"] = self.golesT1
                    partido["golesT2"] = self.golesT2
                    partido["penalesT1"] = self.penalesT1
                    partido["penalesT2"] = self.penalesT2
                    partido["jugado"] = True

                    with open(filename, "w") as file:
                        json.dump(partidos, file, indent=4)

                    # actualizar puntos de los equipos segun el resultado
                    # solo si antes no tenia goles 
                    id_t1 = partido.get("idEquipo1")
                    id_t2 = partido.get("idEquipo2")

                    if prev_g1 == 0 and prev_g2 == 0 and id_t1 and id_t2:
                        equipos = []
                        equipos_file = get_path("data", "equipos.json")
                        if file_exists(equipos_file):
                            with open(equipos_file, "r") as f_eq:
                                if not is_file_empty(equipos_file):
                                    equipos = json.load(f_eq)

                        if len(equipos) != 0:
                            for eq in equipos:
                                eq.setdefault("puntos", 0)
                                if self.golesT1 > self.golesT2:
                                    if eq["id"] == id_t1:
                                        eq["puntos"] += 3
                                elif self.golesT2 > self.golesT1:
                                    if eq["id"] == id_t2:
                                        eq["puntos"] += 3
                                else:
                                    if eq["id"] == id_t1 or eq["id"] == id_t2:
                                        eq["puntos"] += 1

                            with open(equipos_file, "w") as f_eq:
                                json.dump(equipos, f_eq, indent=4)

                    return True
            
        return None
                    

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
                        partidos[partido_index]["fase"] = "Fase de Grupos"
                        partido_index += 1

                    if partido_index >= 72 or partido_index >= len(partidos):
                        break
        
        # guardar cambios
        with open(filename, "w") as file:
            json.dump(partidos, file, indent=4)

    return True


def _fase_por_indice(index: int) -> str:
    if index < 72:
        return "Fase de Grupos"
    if index < 88:
        return "16avos de Final"
    if index < 96:
        return "Octavos de Final"
    if index < 100:
        return "Cuartos de Final"
    if index < 102:
        return "Semifinal"
    if index == 102:
        return "Tercer Puesto"
    return "Final"


def asignar_fases_por_orden(filename: str = None):
    if filename is None:
        filename = PATH

    if not file_exists(filename):
        return False

    with open(filename, "r") as file:
        if is_file_empty(filename):
            return False
        partidos = json.load(file)

    if len(partidos) != 104:
        return False

    for index, partido in enumerate(partidos):
        partido["fase"] = _fase_por_indice(index)

    with open(filename, "w") as file:
        json.dump(partidos, file, indent=4)

    return True


# Se carga una sola vez al importar el modulo; sin costo en cada llamada.
with open(get_path("data", "tabla_anexo_c.json"), "r") as _f:
    _TABLA_ANEXO_C: list[dict] = json.load(_f)

# Índice preconstruido: frozenset de grupos -> orden de slots como lista.
# Permite buscar en O(1) en lugar de iterar las 495 combinaciones cada vez.
# gracias jarvis
_ANEXO_C_INDEX: dict[frozenset, list[str]] = {
    frozenset(entry["combinacion"]): entry["combinacion"]
    for entry in _TABLA_ANEXO_C
}


def _orden_terceros(mejores_terceros: list) -> list[str] | None:
    """
    Dado el pool de mejores terceros clasificados, devuelve la lista ordenada
    de grupos según la tabla del anexo C.

    Retorna la combinacion (lista de grupos en orden de slots) o None si la
    combinación no existe en la tabla.

    Si no existe entonces me quejo en fifa por cojones
    """
    clave = frozenset(eq["grupo"].upper() for eq in mejores_terceros)
    return _ANEXO_C_INDEX.get(clave)


def setEliminatorias(filename: str = None):
    if filename is None:
        filename = PATH

    equipos = equipo.Equipo.getAllEquipos()
    if equipos is None:
        return None

    mejores_equipos = equipo.getMejoresEquiposGrupo()
    if not mejores_equipos or len(mejores_equipos) < 32:
        return None

    ganadores = [eq for eq in mejores_equipos if eq.get("posicion") == 1]
    subcampeones = [eq for eq in mejores_equipos if eq.get("posicion") == 2]
    terceros = [eq for eq in mejores_equipos if eq.get("posicion") == 3]

    if len(ganadores) != 12 or len(subcampeones) != 12 or len(terceros) != 8:
        return None

    mejores_terceros = equipo.ordenar_terceros(terceros)[:8]
    orden_grupos = _orden_terceros(mejores_terceros)
    if orden_grupos is None:
        return None

    tercero_por_grupo = {eq["grupo"].upper(): eq for eq in mejores_terceros}
    iter_terceros = iter(orden_grupos)

    sequence = [
        ('2A', '2B'),
        ('1E', ('best_third', ['A', 'B', 'C', 'D', 'F'])),
        ('1F', '2C'),
        ('1C', '2F'),
        ('1I', ('best_third', ['C', 'D', 'F', 'G', 'H'])),
        ('2E', '2I'),
        ('1A', ('best_third', ['C', 'E', 'F', 'H', 'I'])),
        ('1L', ('best_third', ['E', 'H', 'I', 'J', 'K'])),
        ('1D', ('best_third', ['B', 'E', 'F', 'I', 'J'])),
        ('1G', ('best_third', ['A', 'E', 'H', 'I', 'J'])),
        ('2K', '2L'),
        ('1H', '2J'),
        ('1B', ('best_third', ['E', 'F', 'G', 'I', 'J'])),
        ('1J', '2H'),
        ('1K', ('best_third', ['D', 'E', 'I', 'J', 'L'])),
        ('2D', '2G'),
    ]

    def pick_by_label(label: str):
        """Traduce '1A' -> ganador del grupo A, '2B' -> subcampeon del grupo B."""
        if not label or len(label) < 2:
            return None
        lab = label.strip().upper()
        pos = lab[0]
        grp = lab[1]
        if pos == '1':
            return next((g for g in ganadores    if g['grupo'].upper() == grp), None)
        if pos == '2':
            return next((s for s in subcampeones if s['grupo'].upper() == grp), None)
        return None

    matches = []

    for l, r in sequence:
        if isinstance(l, tuple) and l[0] == 'best_third':
            grupo_asignado = next(iter_terceros, None)
            equipo1 = tercero_por_grupo.get(grupo_asignado) if grupo_asignado else None
        else:
            equipo1 = pick_by_label(l)

        if isinstance(r, tuple) and r[0] == 'best_third':
            grupo_asignado = next(iter_terceros, None)
            equipo2 = tercero_por_grupo.get(grupo_asignado) if grupo_asignado else None
        else:
            equipo2 = pick_by_label(r)

        if equipo1 is None or equipo2 is None:
            return None

        matches.append((equipo1['id'], equipo2['id']))

    partidos = []
    if file_exists(filename):
        with open(filename, "r") as file:
            if not is_file_empty(filename):
                partidos = json.load(file)

    for index, (id1, id2) in enumerate(matches, start=72):
        partidos[index]["idEquipo1"] = id1
        partidos[index]["idEquipo2"] = id2
        partidos[index]["fase"] = "16avos de Final"

    with open(filename, "w") as file:
        json.dump(partidos, file, indent=4)

    return True

def _get_ganador_partido(partidos, id_partido):
    """Retorna el ID del equipo ganador de un partido por goles y penales."""
    p = partidos[id_partido - 1]
    if not p.get("jugado"):
        return None
    g1, g2 = p.get("golesT1", 0), p.get("golesT2", 0)
    if g1 > g2:
        return p["idEquipo1"]
    elif g2 > g1:
        return p["idEquipo2"]
    else:
        p1, p2 = p.get("penalesT1", 0), p.get("penalesT2", 0)
        return p["idEquipo1"] if p1 > p2 else p["idEquipo2"]

def _get_perdedor_partido(partidos, id_partido):
    """Retorna el ID del equipo perdedor de un partido."""
    p = partidos[id_partido - 1]
    if not p.get("jugado"):
        return None
    g1, g2 = p.get("golesT1", 0), p.get("golesT2", 0)
    if g1 > g2:
        return p["idEquipo2"]
    elif g2 > g1:
        return p["idEquipo1"]
    else:
        p1, p2 = p.get("penalesT1", 0), p.get("penalesT2", 0)
        return p["idEquipo2"] if p1 > p2 else p["idEquipo1"]

def setOctavos(filename: str = None):
    if filename is None:
        filename = PATH

    partidos = []
    if file_exists(filename):
        with open(filename, "r") as file:
            if not is_file_empty(filename):
                partidos = json.load(file)

    emparejamientos_octavos = [
        (74, 77), (73, 75), (76, 78), (79, 80),
        (83, 84), (81, 82), (86, 88), (85, 87),
    ]

    for index, (p1, p2) in enumerate(emparejamientos_octavos, start=88):
        g1 = _get_ganador_partido(partidos, p1)
        g2 = _get_ganador_partido(partidos, p2)
        if g1 is None or g2 is None:
            return None
        partidos[index]["idEquipo1"] = g1
        partidos[index]["idEquipo2"] = g2
        partidos[index]["fase"] = "Octavos de Final"

    with open(filename, "w") as file:
        json.dump(partidos, file, indent=4)
    return True


def setCuartos(filename: str = None):
    if filename is None:
        filename = PATH

    partidos = []
    if file_exists(filename):
        with open(filename, "r") as file:
            if not is_file_empty(filename):
                partidos = json.load(file)

    emparejamientos_cuartos = [
        (89, 90), (93, 94), (91, 92), (95, 96),
    ]

    for index, (p1, p2) in enumerate(emparejamientos_cuartos, start=96):
        g1 = _get_ganador_partido(partidos, p1)
        g2 = _get_ganador_partido(partidos, p2)
        if g1 is None or g2 is None:
            return None
        partidos[index]["idEquipo1"] = g1
        partidos[index]["idEquipo2"] = g2
        partidos[index]["fase"] = "Cuartos de Final"

    with open(filename, "w") as file:
        json.dump(partidos, file, indent=4)
    return True


def setSemis(filename: str = None):
    if filename is None:
        filename = PATH

    partidos = []
    if file_exists(filename):
        with open(filename, "r") as file:
            if not is_file_empty(filename):
                partidos = json.load(file)

    emparejamientos_semis = [
        (97, 98), (99, 100),
    ]

    for index, (p1, p2) in enumerate(emparejamientos_semis, start=100):
        g1 = _get_ganador_partido(partidos, p1)
        g2 = _get_ganador_partido(partidos, p2)
        if g1 is None or g2 is None:
            return None
        partidos[index]["idEquipo1"] = g1
        partidos[index]["idEquipo2"] = g2
        partidos[index]["fase"] = "Semifinal"

    with open(filename, "w") as file:
        json.dump(partidos, file, indent=4)
    return True


def setFinal(filename: str = None):
    if filename is None:
        filename = PATH

    partidos = []
    if file_exists(filename):
        with open(filename, "r") as file:
            if not is_file_empty(filename):
                partidos = json.load(file)

    def get_ganador(id_partido):
        p = partidos[id_partido - 1]
        if not p.get("jugado"):
            return None
        g1, g2 = p.get("golesT1", 0), p.get("golesT2", 0)
        if g1 > g2:
            return p["idEquipo1"]
        elif g2 > g1:
            return p["idEquipo2"]
        else:
            p1, p2 = p.get("penalesT1", 0), p.get("penalesT2", 0)
            return p["idEquipo1"] if p1 > p2 else p["idEquipo2"]

    def get_perdedor(id_partido):
        p = partidos[id_partido - 1]
        if not p.get("jugado"):
            return None
        g1, g2 = p.get("golesT1", 0), p.get("golesT2", 0)
        if g1 > g2:
            return p["idEquipo2"]
        elif g2 > g1:
            return p["idEquipo1"]
        else:
            p1, p2 = p.get("penalesT1", 0), p.get("penalesT2", 0)
            return p["idEquipo2"] if p1 > p2 else p["idEquipo1"]

    # M103 (index 102): tercer puesto -> perdedores de SF1(101) y SF2(102)
    perdedor_sf1 = _get_perdedor_partido(partidos, 101)
    perdedor_sf2 = _get_perdedor_partido(partidos, 102)
    if perdedor_sf1 is None or perdedor_sf2 is None:
        return None
    partidos[102]["idEquipo1"] = perdedor_sf1
    partidos[102]["idEquipo2"] = perdedor_sf2
    partidos[102]["fase"] = "Tercer Puesto"

    # M104 (index 103): final -> ganadores de SF1(101) y SF2(102)
    ganador_sf1 = _get_ganador_partido(partidos, 101)
    ganador_sf2 = _get_ganador_partido(partidos, 102)
    if ganador_sf1 is None or ganador_sf2 is None:
        return None
    partidos[103]["idEquipo1"] = ganador_sf1
    partidos[103]["idEquipo2"] = ganador_sf2
    partidos[103]["fase"] = "Final"

    with open(filename, "w") as file:
        json.dump(partidos, file, indent=4)

    return True