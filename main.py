import customtkinter as tk
from models import equipo, partido, torneo
from ui.app import *
from ui.views.btnHandler import *

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
btn1 = tk.CTkButton(parent, text="Configuración del Torneo", width=200, height=50, command=lambda: open_torneo_config(root))
btn1.pack(pady=10)

btn2 = tk.CTkButton(parent, text="Registro de Resultados", width=200, height=50)
btn2.pack(pady=10)

btn3 = tk.CTkButton(parent, text="Emisión de Informes", width=200, height=50)
btn3.pack(pady=10)

# el destroy es una funcion nativa del tkinter, para cerrar
btn4 = tk.CTkButton(parent, text="Salir", width=200, height=50, command=root.destroy)
btn4.pack(pady=10)
# hasta aca llegan los botones


# bs que inicia la app
root.mainloop()
