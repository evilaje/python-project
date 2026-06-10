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
            with open(filename, "r", encoding="utf-8") as file:
                if not is_file_empty(filename):
                    partidos = json.load(file)

        partidos.append(self.toDict())

        from datetime import datetime
        try:
            partidos.sort(key=lambda partido: datetime.strptime(
                f"{partido.get('fecha', '').strip()} {partido.get('hora', '').strip()}",
                "%d/%m/%Y %H:%M"
            ))
        except Exception:
            pass

        for index, partido in enumerate(partidos, start=1):
            partido["id"] = index
            if (partido.get("fecha") == self.fecha and
                partido.get("hora") == self.hora and
                partido.get("lugar") == self.lugar and
                partido.get("idEquipo1") == self.idEquipo1 and
                partido.get("idEquipo2") == self.idEquipo2 and
                partido.get("golesT1") == self.golesT1 and
                partido.get("golesT2") == self.golesT2 and
                partido.get("penalesT1") == self.penalesT1 and
                partido.get("penalesT2") == self.penalesT2 and
                partido.get("fase") == self.fase and
                partido.get("jugado") == self.jugado):
                self.id = index

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(partidos, file, indent=4)

        # aumentar los puntos de los equipos segun el resultado
        equipos = []
        with open(get_path("data", "equipos.json"), "r", encoding="utf-8") as file:
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

            with open(get_path("data", "equipos.json"), "w", encoding="utf-8") as file:
                json.dump(equipos, file, indent=4)


    # esto es para el autoincrement
    def obtenerId(self, filename=None):
        if (filename is None):
            filename = PATH

        if not file_exists(filename): #por si el archivo todavia no se creo
            return 1

        with open(filename, "r", encoding="utf-8") as file:
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
            with open(filename, "r", encoding="utf-8") as file:
                arr = json.load(file)
                for reg in arr:
                    if self.id == reg["id"]:
                        self.idEquipo1 = idT1
                        self.idEquipo2 = idT2
                        reg["idEquipo1"] = self.idEquipo1
                        reg["idEquipo2"] = self.idEquipo2

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(arr, file, indent=4)

        return None


    # al abrir la app se cargar todo en un arreglo
    @staticmethod
    def getAllPartidos(filename:str = None):
        if (filename is None):
            filename = PATH
        arr = []
        if (file_exists(filename)):
            with open(filename, "r", encoding="utf-8") as file:
                if not is_file_empty(filename):
                    arr = json.load(file)
                    return arr if len(arr) > 0 else None
        print("No se ha leido ningun partido papi")
        return None
    
    @staticmethod
    def getPartidosPendientes(filename: str = None):
        if filename is None:
            filename = PATH
        if file_exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                if not is_file_empty(filename):
                    arr = json.load(file)
                    pendientes = [p for p in arr if p.get("jugado") == False]
                    return pendientes if len(pendientes) > 0 else None
        print("No se ha leido ningun partido papi")
        return None


    @staticmethod
    def ordenar_partidos_por_fecha_y_reasignar_ids(filename:str = None):
        if (filename is None):
            filename = PATH
        if not file_exists(filename):
            return False

        with open(filename, "r", encoding="utf-8") as file:
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

        with open(filename, "w", encoding="utf-8") as file:
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
            with open(filename, "r", encoding="utf-8") as file:
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

                    with open(filename, "w", encoding="utf-8") as file:
                        json.dump(partidos, file, indent=4)

                    # actualizar puntos de los equipos segun el resultado
                    # solo si antes no tenia goles
                    id_t1 = partido.get("idEquipo1")
                    id_t2 = partido.get("idEquipo2")

                    if prev_g1 == 0 and prev_g2 == 0 and id_t1 and id_t2:
                        equipos = []
                        equipos_file = get_path("data", "equipos.json")
                        if file_exists(equipos_file):
                            with open(equipos_file, "r", encoding="utf-8") as f_eq:
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

                            with open(equipos_file, "w", encoding="utf-8") as f_eq:
                                json.dump(equipos, f_eq, indent=4)

                    return True

        return None


def getPartido(id, filename:str = None):
    if (filename is None):
        filename = PATH
    arr = []
    if (file_exists(filename)):
        with open(filename, "r", encoding="utf-8") as file:
            if not is_file_empty(filename):
                arr = json.load(file)
    for obj in arr:
        if (id == obj["id"]): return obj
    return None

# una jornada es una semana -> 2 partidos por grupo
# 24 partidos por jornada
# vamos a suponer que esta validado en el front que solo pueden haber 24 partidos por jornada
# porque no pienso hacer aca eso

def setEquiposFaseGrupos(filename: str = None):
    if filename is None:
        filename = PATH

    equipos = equipo.Equipo.getAllEquipos()
    if equipos is None:
        return None

    # Organizar equipos por grupo ordenados por id (A1 < A2 < A3 < A4)
    grupos = {}
    for eq in equipos:
        grupos.setdefault(eq["grupo"], []).append(eq)

    for grupo in grupos:
        grupos[grupo].sort(key=lambda x: x["id"])

    # Verificar que todos los grupos tienen exactamente 4 equipos
    for g in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]:
        if len(grupos.get(g, [])) != 4:
            return None

    # Índice de acceso rápido: (grupo, posición) -> id del equipo
    # Posición 1 = primer equipo del grupo (A1), 2 = A2, etc.
    idx = {}
    for grupo, lista in grupos.items():
        for pos, eq in enumerate(lista, start=1):
            idx[(grupo, pos)] = eq["id"]

    # Secuencia oficial del fixture del Mundial 2026 — orden cronológico de los 72 partidos
    # Cada tupla: (grupo, posicion_equipo1, posicion_equipo2)
    fixture = [
        # Jornada 1
        ('A', 1, 2), ('A', 3, 4),                            # Jun 11
        ('B', 1, 2), ('D', 1, 2),                            # Jun 12
        ('B', 3, 4), ('C', 1, 2), ('C', 3, 4), ('D', 3, 4), # Jun 13
        ('E', 1, 2), ('F', 1, 2), ('E', 3, 4), ('F', 3, 4), # Jun 14
        ('H', 1, 2), ('G', 1, 2), ('H', 3, 4), ('G', 3, 4), # Jun 15
        ('I', 1, 2), ('I', 3, 4), ('J', 1, 2), ('J', 3, 4), # Jun 16
        ('K', 1, 2), ('L', 1, 2), ('L', 3, 4), ('K', 3, 4),# Jun 17
        # j2
        ('A', 4, 2), ('B', 4, 2), ('B', 1, 3), ('A', 1, 3),# Jun 18
        ('D', 1, 3), ('C', 4, 2), ('C', 1, 3), ('D', 4, 2), # Jun 19
        ('F', 1, 3), ('E', 1, 3), ('E', 4, 2), ('F', 4, 2), # Jun 20
        ('H', 1, 3), ('G', 1, 3), ('H', 4, 2), ('G', 4, 2), # Jun 21
        ('J', 1, 3), ('I', 1, 3), ('I', 4, 2), ('J', 4, 2), # Jun 22
        ('K', 1, 3), ('L', 1, 3), ('L', 4, 2), ('K', 4, 2), # Jun 23
        ('B', 4, 1), ('B', 2, 3), ('C', 4, 1), ('C', 2, 3), # Jun 24
        ('A', 4, 1), ('A', 2, 3),
        ('E', 2, 3), ('E', 4, 1), ('F', 2, 3), ('F', 4, 1), # Jun 25
        ('D', 4, 1), ('D', 2, 3),
        ('I', 4, 1), ('I', 2, 3), ('H', 2, 3), ('H', 4, 1), # Jun 26
        ('G', 2, 3), ('G', 4, 1),
        ('L', 4, 1), ('L', 2, 3), ('K', 4, 1), ('K', 2, 3), # Jun 27
        ('J', 2, 3), ('J', 4, 1),
    ]

    if not file_exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as file:
        if is_file_empty(filename):
            return None
        partidos = json.load(file)

    if len(partidos) < 72:
        return None

    for partido_index, (grupo, p1, p2) in enumerate(fixture):
        partidos[partido_index]["idEquipo1"] = idx[(grupo, p1)]
        partidos[partido_index]["idEquipo2"] = idx[(grupo, p2)]
        partidos[partido_index]["fase"] = "Fase de Grupos"

    with open(filename, "w", encoding="utf-8") as file:
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

    with open(filename, "r", encoding="utf-8") as file:
        if is_file_empty(filename):
            return False
        partidos = json.load(file)

    if len(partidos) != 104:
        return False

    for index, partido in enumerate(partidos):
        partido["fase"] = _fase_por_indice(index)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(partidos, file, indent=4)

    return True


# Se carga una sola vez al importar el modulo; sin costo en cada llamada.
with open(get_path("data", "tabla_anexo_c.json"), "r", encoding="utf-8") as _f:
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
        with open(filename, "r", encoding="utf-8") as file:
            if not is_file_empty(filename):
                partidos = json.load(file)

    for index, (id1, id2) in enumerate(matches, start=72):
        partidos[index]["idEquipo1"] = id1
        partidos[index]["idEquipo2"] = id2
        partidos[index]["fase"] = "16avos de Final"

    with open(filename, "w", encoding="utf-8") as file:
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
        with open(filename, "r", encoding="utf-8") as file:
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

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(partidos, file, indent=4)
    return True


def setCuartos(filename: str = None):
    if filename is None:
        filename = PATH

    partidos = []
    if file_exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
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

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(partidos, file, indent=4)
    return True


def setSemis(filename: str = None):
    if filename is None:
        filename = PATH

    partidos = []
    if file_exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
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

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(partidos, file, indent=4)
    return True


def setFinal(filename: str = None):
    if filename is None:
        filename = PATH

    partidos = []
    if file_exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
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

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(partidos, file, indent=4)

    return True

def getAllPartidos(filename = None):
    if (filename is None):
        filename = PATH
    arr = []
    if (file_exists(filename)):
        with open(filename, "r", encoding="utf-8") as file:
            if not is_file_empty(filename):
                arr = json.load(file)
    return arr if len(arr) != 0 else None

def getPartidosPorFecha(str_fecha:str):
    partidos = getAllPartidos()
    partidos_retorno = []
    if partidos:
        for p in partidos:
            if p["fecha"] == str_fecha:
                partidos_retorno.append(p)
    return partidos_retorno
