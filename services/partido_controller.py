from models.partido import *
from models.partido import _get_ganador_partido, _get_perdedor_partido
import models.partido as partido
import models.torneo as torneo
import models.equipo as equipo


def cargarPartido(fecha:str, hora:str, lugar:str):
    # validar que no se superen los 104 partidos
    partidos = Partido.getAllPartidos() or []
    if len(partidos) >= 104:
        return False, "Ya hay 104 partidos cargados. No se pueden agregar más."

    #validaciones hechas en los controllers/front, por eso aca na de na
    t = torneo.getTorneo(1)

    partido:Partido = Partido(fecha, hora, lugar)
    partido.savePartido()
    return True, "Exito"

def guardarResultado(id: int, g1: int, g2: int, gp1: int, gp2: int):
    partido = Partido(None, None, None)
    partido.id = id
    partido.golesT1 = g1
    partido.golesT2 = g2
    partido.penalesT1 = gp1
    partido.penalesT2 = gp2


    if partido.setGoles():
        # Después de guardar el resultado, actualizar fases de equipos según la fase del partido
        try:
            partidos = Partido.getAllPartidos() or []
            p = getPartido(id)
            if p:
                fase = p.get("fase")
                print(f"DEBUG: Actualizando fases para partido {id} en fase '{fase}'")
                # obtener ganador y perdedor
                ganador = _get_ganador_partido(partidos, id)
                perdedor = _get_perdedor_partido(partidos, id)
                print(f"DEBUG: Ganador: {ganador}, Perdedor: {perdedor}")

                # Mapeo de avance para rondas de eliminatoria (estado legible)
                next_phase_map = {
                    "16avos de Final": "Clasificado a Octavos de Final",
                    "Octavos de Final": "Clasificado a Cuartos de Final",
                    "Cuartos de Final": "Clasificado a Semifinales",
                }

                eliminacion_map = {
                    "16avos de Final": "Eliminado en 16avos de Final",
                    "Octavos de Final": "Eliminado en Octavos de Final",
                    "Cuartos de Final": "Eliminado en Cuartos de Final",
                }

                if fase in next_phase_map:
                    if ganador:
                        new_fase = next_phase_map[fase]
                        equipo.setEquipoFase(ganador, new_fase)
                        print(f"DEBUG: {ganador} actualizado a '{new_fase}'")
                    if perdedor:
                        new_fase_elim = eliminacion_map[fase]
                        equipo.setEquipoFase(perdedor, new_fase_elim)
                        print(f"DEBUG: {perdedor} actualizado a '{new_fase}'")

                elif fase == "Semifinal":
                    # Ganador -> Finalista, perdedor -> Partido por el 3er puesto
                    if ganador:
                        equipo.setEquipoFase(ganador, "Finalista")
                        print(f"DEBUG: {ganador} actualizado a 'Finalista'")
                    if perdedor:
                        equipo.setEquipoFase(perdedor, "Partido por el 3er puesto")
                        print(f"DEBUG: {perdedor} actualizado a 'Partido por el 3er puesto'")

                elif fase == "Tercer Puesto":
                    # Ganador -> Tercer Puesto, Perdedor -> Cuarto Puesto
                    if ganador:
                        equipo.setEquipoFase(ganador, "Tercer Puesto")
                        print(f"DEBUG: {ganador} actualizado a 'Tercer Puesto'")
                    if perdedor:
                        equipo.setEquipoFase(perdedor, "Cuarto Puesto")
                        print(f"DEBUG: {perdedor} actualizado a 'Cuarto Puesto'")

                elif fase == "Final":
                    # Ganador -> Primer Puesto, Perdedor -> Segundo Puesto
                    if ganador:
                        equipo.setEquipoFase(ganador, "Primer Puesto")
                        print(f"DEBUG: {ganador} actualizado a 'Primer Puesto'")
                    if perdedor:
                        equipo.setEquipoFase(perdedor, "Segundo Puesto")
                        print(f"DEBUG: {perdedor} actualizado a 'Segundo Puesto'")
        except Exception as e:
            # no bloquear la respuesta si algo falla al actualizar equipos
            print(f"DEBUG: Error al actualizar fases: {e}")
            pass

        return [True, "Exito"]

    return [False, "No se pudo guardar el resultado"]

def getPartidoPorFecha(fecha:str):
    # fecha expected format: "DD/MM/AAAA" (exact match)
    partidos = Partido.getAllPartidos()
    if not partidos:
        return []

    resultados = []
    for p in partidos:
        if not p.get("fecha"):
            continue
        if p["fecha"].strip() != fecha.strip():
            continue

        # obtener nombres de equipos
        local = None
        visitante = None
        if p.get("idEquipo1"):
            eq1 = equipo.getEquipo(p.get("idEquipo1"))
            local = eq1.get("pais") if eq1 else p.get("idEquipo1")
        else:
            local = "Por definir"

        if p.get("idEquipo2"):
            eq2 = equipo.getEquipo(p.get("idEquipo2"))
            visitante = eq2.get("pais") if eq2 else p.get("idEquipo2")
        else:
            visitante = "Por definir"

        # Usar la fase tal como está registrada en el partido (partidos.json)
        fase = p.get("fase") or "Fase de Grupos"

        resultados.append({
            "fecha": p.get("fecha"),
            "hora": p.get("hora", ""),
            "local": local,
            "visitante": visitante,
            "fase": fase,
            "lugar": p.get("lugar", "")
        })

    # ordenar por hora
    try:
        resultados.sort(key=lambda x: x.get("hora", ""))
    except Exception:
        pass

    return resultados


def getPartidosPorEquipo(equipo_nombre: str):
    equipos = equipo.Equipo.getAllEquipos()
    if not equipos:
        return {"partidos": [], "clasificacion": None}

    equipo_obj = next((e for e in equipos if e.get("pais", "").strip().lower() == equipo_nombre.strip().lower()), None)
    if not equipo_obj:
        return {"partidos": [], "clasificacion": None}

    equipo_id = equipo_obj.get("id")
    grupo = equipo_obj.get("grupo")
    partidos = Partido.getAllPartidos() or []

    resultado = []
    for p in partidos:
        if p.get("idEquipo1") != equipo_id and p.get("idEquipo2") != equipo_id:
            continue

        rival_id = p.get("idEquipo2") if p.get("idEquipo1") == equipo_id else p.get("idEquipo1")
        rival = equipo.getEquipo(rival_id)
        rival_nombre = rival.get("pais") if rival else rival_id or "Por definir"

        goles_local = p.get("golesT1", 0) if p.get("idEquipo1") == equipo_id else p.get("golesT2", 0)
        goles_visit = p.get("golesT2", 0) if p.get("idEquipo1") == equipo_id else p.get("golesT1", 0)

        # Usar la fase tal como está registrada en el partido (partidos.json)
        fase = p.get("fase") or "Fase de Grupos"

        resultado.append({
            "fecha": p.get("fecha"),
            "hora": p.get("hora", ""),
            "fase": fase,
            "local": equipo_nombre,
            "visitante": rival_nombre,
            "golesLocal": goles_local,
            "golesVisit": goles_visit
        })

    # ordenar por fecha y hora si están disponibles
    try:
        from datetime import datetime
        resultado.sort(key=lambda x: datetime.strptime(f"{x.get('fecha', '')} {x.get('hora', '00:00')}", "%d/%m/%Y %H:%M") if x.get('fecha') else datetime.max)
    except Exception:
        pass

    clasificacion = None
    if grupo and grupo != "placeholder":
        # construir tabla del grupo para clasificar
        grupo_ids = [e["id"] for e in equipos if e.get("grupo") == grupo]
        tabla = {team_id: {"pts": 0, "dg": 0, "gf": 0, "gc": 0, "pj": 0} for team_id in grupo_ids}

        for p in partidos:
            id1 = p.get("idEquipo1")
            id2 = p.get("idEquipo2")
            if id1 not in tabla or id2 not in tabla:
                continue

            g1 = p.get("golesT1", 0)
            g2 = p.get("golesT2", 0)
            if g1 == 0 and g2 == 0 and p.get("penalesT1", 0) == 0 and p.get("penalesT2", 0) == 0:
                continue

            tabla[id1]["pj"] += 1
            tabla[id2]["pj"] += 1
            tabla[id1]["gf"] += g1
            tabla[id1]["gc"] += g2
            tabla[id2]["gf"] += g2
            tabla[id2]["gc"] += g1
            tabla[id1]["dg"] = tabla[id1]["gf"] - tabla[id1]["gc"]
            tabla[id2]["dg"] = tabla[id2]["gf"] - tabla[id2]["gc"]

            if g1 > g2:
                tabla[id1]["pts"] += 3
            elif g2 > g1:
                tabla[id2]["pts"] += 3
            else:
                tabla[id1]["pts"] += 1
                tabla[id2]["pts"] += 1

        if all(v["pj"] >= 3 for v in tabla.values()):
            orden = sorted(
                tabla.items(),
                key=lambda item: (item[1]["pts"], item[1]["dg"], item[1]["gf"]),
                reverse=True
            )
            posicion = next((i + 1 for i, (team_id, _) in enumerate(orden) if team_id == equipo_id), None)
            if posicion is not None:
                if posicion <= 2:
                    clasificacion = "Clasificado a Octavos de Final"
                else:
                    clasificacion = "Eliminado de la fase de grupos"

    return {"partidos": resultado, "clasificacion": clasificacion}


def getSiguientePartido(equipo_nombre: str):
    equipos = equipo.Equipo.getAllEquipos()
    if not equipos:
        return None

    equipo_obj = next((e for e in equipos if e.get("pais", "").strip().lower() == equipo_nombre.strip().lower()), None)
    if not equipo_obj:
        return None

    equipo_id = equipo_obj.get("id")
    partidos = Partido.getAllPartidos() or []

    proximos = []
    from datetime import datetime
    ahora = datetime.now()

    for p in partidos:
        if p.get("idEquipo1") != equipo_id and p.get("idEquipo2") != equipo_id:
            continue

        fecha = p.get("fecha")
        hora = p.get("hora", "00:00")
        if not fecha:
            continue

        try:
            dt = datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")
        except Exception:
            continue

        if dt <= ahora or p["jugado"] == True:
            continue

        proximos.append((dt, p))

    if not proximos:
        return None

    proximos.sort(key=lambda item: item[0])
    proximo = proximos[0][1]

    torneo_obj = torneo.getTorneo(1)
    torneo_nombre = torneo_obj.get("nombre") if torneo_obj else "Torneo"
    fecha = proximo.get("fecha")
    hora = proximo.get("hora", "")

    eq1 = equipo.getEquipo(proximo.get("idEquipo1"))
    eq2 = equipo.getEquipo(proximo.get("idEquipo2"))


    partido_info = {
        "torneo": torneo_nombre,
        "fase": proximo.get("fase") or "Fase de Grupos",
        "lugar": proximo.get("lugar", ""),
        "fecha": fecha,
        "hora": hora,
        "local": eq1.get("pais") if eq1 else proximo.get("idEquipo1") or "Por definir",
        "visitante": eq2.get("pais") if eq2 else proximo.get("idEquipo2") or "Por definir",
        "local_abrev": eq1.get("abreviatura", "") if eq1 else "",
        "visitante_abrev": eq2.get("abreviatura", "") if eq2 else "",
    }


    # Usar la fase tal como está registrada en el partido (partidos.json)

    return partido_info


def getSiguienteGeneral():
    """Retorna el próximo partido (sin filtrar por equipo).
    Devuelve None si no hay próximos partidos.
    """
    partidos = Partido.getAllPartidos() or []
    proximos = []
    from datetime import datetime
    ahora = datetime.now()

    for p in partidos:
        fecha = p.get("fecha")
        hora = p.get("hora", "00:00")
        if not fecha:
            continue
        try:
            dt = datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")
        except Exception:
            continue

        if dt <= ahora:
            continue

        proximos.append((dt, p))

    if not proximos:
        return None

    proximos.sort(key=lambda item: item[0])
    proximo = proximos[0][1]

    torneo_obj = torneo.getTorneo(1)
    torneo_nombre = torneo_obj.get("nombre") if torneo_obj else "Torneo"

    eq1 = equipo.getEquipo(proximo.get("idEquipo1"))
    eq2 = equipo.getEquipo(proximo.get("idEquipo2"))
    local_nombre = eq1.get("pais") if eq1 else proximo.get("idEquipo1") or "Por definir"
    visitante_nombre = eq2.get("pais") if eq2 else proximo.get("idEquipo2") or "Por definir"

    return {
        "partido": proximo,
        "torneo": torneo_nombre,
        "fecha": proximo.get("fecha"),
        "hora": proximo.get("hora", ""),
        "local": local_nombre,
        "visitante": visitante_nombre,
        "lugar": proximo.get("lugar", ""),
        "fase": proximo.get("fase", "")
    }
