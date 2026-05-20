from models.partido import *
import models.torneo as torneo
import models.equipo as equipo


def cargarPartido(fecha:str, hora:str, lugar:str):
    #validaciones hechas en los controllers/front, por eso aca na de na
    t = torneo.getTorneo(1)

    # validar esto

    partido:Partido = Partido(fecha, hora, lugar)
    partido.savePartido()
    
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

        # determinar fase (si alguno de los equipos ya está en eliminatorias, marcar eliminatorias)
        fase = "Fase de Grupos"
        if (p.get("idEquipo1") and p.get("idEquipo2")):
            eq1 = equipo.getEquipo(p.get("idEquipo1"))
            eq2 = equipo.getEquipo(p.get("idEquipo2"))
            if (eq1 and eq1.get("fase") == "eliminatorias") or (eq2 and eq2.get("fase") == "eliminatorias"):
                fase = "Eliminatorias"

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
