import customtkinter as tk

from ui.app import *
from ui.views.configHandler import *
from ui.views.resultsHandler import *
from ui.views.reportHandler import *

from models.partido import *
from models.equipo import *
from models.torneo import *

print("test")
t1 = Torneo("Copa America", "10/05/2026", "14/05/2026")
t1.saveTorneo()
p1 = Partido("14/05/2026", "12:00", "La nueva Olla", 1, 1)
p1.savePartido()
eq1 = Equipo("P1", "Paraguay", "PY", "+595", "FIFA", "A")
eq2 = Equipo("P2", "Argentina", "ARG", "+54", "CONMEBOL", "A")
eq3 = Equipo("P3", "Brasil", "BRA", "+55", "CONMEBOL", "B")
eq4 = Equipo("P4", "Uruguay", "URY", "+598", "CONMEBOL", "B")
eq5 = Equipo("P5", "España", "ESP", "+34", "UEFA", "C")
eq6 = Equipo("P6", "Francia", "FRA", "+33", "UEFA", "C")
eq7 = Equipo("P7", "Alemania", "GER", "+49", "UEFA", "D")
eq8 = Equipo("P8", "Italia", "ITA", "+39", "UEFA", "D")
eq9 = Equipo("P9", "Nigeria", "NGA", "+234", "CAF", "E")
eq10 = Equipo("P10", "Senegal", "SEN", "+221", "CAF", "E")
eq10 = Equipo("E1", "Pais de pruba", "PRUEB", "+67", "TTT", "A")
eq1.saveEquipo()
eq2.saveEquipo()
eq3.saveEquipo()
eq4.saveEquipo()
eq5.saveEquipo()
eq6.saveEquipo()
eq7.saveEquipo()
eq8.saveEquipo()
eq9.saveEquipo()
eq10.saveEquipo()

equipos = Equipo.getAllEquipos()
torneos = Torneo.getAllTorneos()
partidos = Partido.getAllPartidos()
print(equipos)
print(torneos)
print(partidos)
# ventana principal
root = App()

# esto crea un frame, un div del html basicamente, donde centras los otros widgets
# para que se vea mas ordenado nomas es
parent = tk.CTkFrame(root)
parent.pack(pady=20, padx=60, fill="both", expand=True)


# este bloque son botones nomas

# lambda: es basicamente para que la funcion no se ejecute cuando corres la app
# normalmente en command pasas el nombre de la funcion sin los parentesis pero si necesitas
# mandarle un parametro tenes que ponerle el lambda para que espere el trigger de tocar el boton
btn1 = tk.CTkButton(parent, text="Configuración del Torneo", height=50, command=lambda: open_torneo_config(root))
btn1.pack(pady=10, padx=10, fill="x")


# segun el pdf este boton se tiene que habilitar cuando ya esten cargados todos los datos (?)
btn2 = tk.CTkButton(parent, text="Registro de Resultados", height=50, state="disabled", command=lambda: open_results_handler(root))
btn2.pack(pady=10, padx=10, fill="x")

btn3 = tk.CTkButton(parent, text="Emisión de Informes", height=50, state="disabled", command=lambda: open_report_handler(root))
btn3.pack(pady=10, padx=10, fill="x")

# el destroy es una funcion nativa del tkinter, para cerrar
btn4 = tk.CTkButton(parent, text="Salir", height=50, command=root.destroy)
btn4.pack(pady=10, padx=10, fill="x")
# hasta aca llegan los botones


# para probar bs
#btn5 = tk.CTkButton(parent, text="Debug", height=50, command=lambda: test.savePartido())
#btn5.pack(pady=10, padx=10, fill="x")


# bs que inicia la app
root.mainloop()
