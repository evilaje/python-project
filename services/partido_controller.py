from models.partido import *
import models.torneo as torneo
import models.equipo as equipo


def cargarPartido(fecha:str, hora:str, lugar:str):
    #validaciones hechas en los controllers/front, por eso aca na de na
    t = torneo.getTorneo(1)

    partido:Partido = Partido(fecha, hora, lugar)
    partido.savePartido()

def guardarResultado(id: int, g1: int, g2: int, gp1: int, gp2: int):
    partido = Partido(None, None, None)
    partido.id = id
    partido.golesT1 = g1
    partido.golesT2 = g2
    partido.penalesT1 = gp1
    partido.penalesT2 = gp2


    if partido.setGoles():
        return [True, "Exito"]

    # true, mensaje
    return [True, "Cagada"]
    
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

        if dt <= ahora:
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
    local_abrev = eq1.get("abreviatura") if eq1 and eq1.get("abreviatura") else eq1.get("pais") if eq1 else proximo.get("idEquipo1") or "Por definir"
    visitante_abrev = eq2.get("abreviatura") if eq2 and eq2.get("abreviatura") else eq2.get("pais") if eq2 else proximo.get("idEquipo2") or "Por definir"

    partido_info = {
        "torneo": torneo_nombre,
        "fase": proximo.get("fase") or "Fase de Grupos",
        "lugar": proximo.get("lugar", ""),
        "fecha": fecha,
        "hora": hora,
        "local": local_abrev,
        "visitante": visitante_abrev
    }

    # Usar la fase tal como está registrada en el partido (partidos.json)

    return partido_info
