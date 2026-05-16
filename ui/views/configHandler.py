import customtkinter as tk
from services.torneo_controller import *
from datetime import datetime
# este es para los popUps, ponele un title, mensaje y icon nomas, icon acepta las palabras cancel, warning y check
from CTkMessagebox import CTkMessagebox


class TorneoConfigFrame(tk.CTkFrame):
    def __init__(self, root, main_frame):
        super().__init__(root)
        self.root = root
        self.main_frame = main_frame

        tk.CTkLabel(self, text="Configuración del Torneo").pack(pady=20, padx=20)

        # Campo nombre
        tk.CTkLabel(self, text="Nombre del Torneo").pack()
        self.input_nombre = tk.CTkEntry(self, placeholder_text="Ej: Copa Mundial 2026")
        self.input_nombre.pack(pady=5, padx=20, fill="x")

        # Campo fecah inicio
        tk.CTkLabel(self, text="Fecha de Inicio").pack()
        self.input_fecha_inicio = tk.CTkEntry(self, placeholder_text="DD/MM/AAAA")
        self.input_fecha_inicio.pack(pady=5, padx=20, fill="x")

        # Campo fecha fin
        tk.CTkLabel(self, text="Fecha de Fin").pack()
        self.input_fecha_fin = tk.CTkEntry(self, placeholder_text="DD/MM/AAAA")
        self.input_fecha_fin.pack(pady=5, padx=20, fill="x")

        tk.CTkButton(self, text="Guardar datos", command=self.guardar_data_torneo).pack(pady=10)
        #tk.CTkButton(self, text="Grupos").pack(pady=10)
        #tk.CTkButton(self, text="Equipos").pack(pady=10)
        #tk.CTkButton(self, text="Calendario").pack(pady=10)

        tk.CTkButton(self, text="Cerrar Configuración", command=self.cerrar_config).pack(pady=10)
        tk.CTkButton(self, text="Volver", command=self.volver).pack(pady=10)

    def guardar_data_torneo(self):
        nombre = self.input_nombre.get().strip()
        fecha_inicio = self.input_fecha_inicio.get().strip()
        fecha_fin = self.input_fecha_fin.get().strip()

        # salta error si algun campo esta vacio
        if not nombre or not fecha_inicio or not fecha_fin:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return

        # validar formato de fecha
        try:
            dt_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            dt_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        except ValueError:
            CTkMessagebox(title="Error", message="Formato de fecha invalido, usa DD/MM/AAAA", icon="cancel")
            return

        # fecha inicio no puede ser antes de hoy
        hoy = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        if dt_inicio < hoy:
            CTkMessagebox(title="Error", message="La fecha de inicio no puede ser anterior a hoy", icon="cancel")
            return

        # fecha fin no puede ser antes o igual que fecha inicio
        if dt_fin <= dt_inicio:
            CTkMessagebox(title="Error", message="La fecha de fin debe ser posterior a la de inicio", icon="cancel")
            return

        cargarTorneo(nombre, fecha_inicio, fecha_fin)
        CTkMessagebox(title="Exito", message="Torneo guardado correctamente", icon="check")


        

    def cerrar_config(self):
        self.main_frame.habilitar_botones()
        self.root.back_to_main(self)

    def volver(self):
        self.root.back_to_main(self)