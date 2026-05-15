import customtkinter as tk

from ui.app import *
from ui.views.configHandler import *
from ui.views.resultsHandler import *
from ui.views.reportHandler import *

from models.partido import *
from models.equipo import *
from models.torneo import *

avanzarFase()


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
btn1 = tk.CTkButton(parent, text="Configuración del Torneo", height=50)
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

# tengo que configurar aca abajo porque crashea sino
# es tipo que como importaba main ahi en configHandler e importaba configHandler aca se volvia loco todo
btn1.configure(command=lambda: open_torneo_config(root, btn1, btn2, btn3))


# para probar bs
#btn5 = tk.CTkButton(parent, text="Debug", height=50, command=lambda: test.savePartido())
#btn5.pack(pady=10, padx=10, fill="x")


# bs que inicia la app
root.mainloop()
