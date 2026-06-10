from tkcalendar import DateEntry
import models.torneo as Torneo
import models.partido as Partido
from datetime import datetime

def str_a_date(fecha_str: str):
    return datetime.strptime(fecha_str, "%d/%m/%Y").date()

def getRangoFechaTorneo():
	t:Torneo = Torneo.getTorneo(1)
	t_ini = str_a_date(t["inicio"])
	t_fin = str_a_date(t["fin"])

	return (t_ini, t_fin)

def datePickerConRango(root, rango, fontS:int = 20):
	fecha = DateEntry(
		root,
		width=15,
		mindate=rango[0],
		maxdate=rango[1],
		date_pattern="dd/mm/yyyy",
		font=("Segoe UI", fontS),
		background="#2b5797",
		foreground="white",
		borderwidth=2
	)

	return fecha

def datePickerComun(root):
	fecha = DateEntry(
		root,
		date_pattern="dd/mm/yyyy",
		font=("Segoe UI", 20),
		background="#2b5797",
		foreground="white",
		borderwidth=2
	)

	return fecha

def date_to_str(date):
	return date.strftime("%d/%m/%Y")

def date_to_partes(d):
	return d.day, d.month, d.year

def isDateLLenoDePartidos(str_date):
	count = len(Partido.getPartidosPorFecha(str_date))
	if count>= 4:
		return True
	return False

def horarioValido(str_hora, str_date):
    hora, min = str_hora.split(":")
    nuevaHora = int(hora) * 60 + int(min)

    partidos = Partido.getPartidosPorFecha(str_date)
    for p in partidos:
        horaTemp, minTemp = p["hora"].split(":")
        horaExistente = int(horaTemp) * 60 + int(minTemp)

        if abs(nuevaHora - horaExistente) < 120:  # 120 minutos = 2 horas, se puede cambiar pero x
            return False, f"El horario del partido choca con otro a las{p['hora']}"

    return True, None
