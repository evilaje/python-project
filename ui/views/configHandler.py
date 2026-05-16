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

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        """vista 1 - torneo"""
        self.frame_torneo = tk.CTkFrame(self, fg_color="transparent")
        self.frame_torneo.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

        self.frame_torneo.grid_columnconfigure(0, weight=1)
        self.frame_torneo.grid_columnconfigure(1, weight=2)
        self.frame_torneo.grid_columnconfigure(2, weight=1)
        self.frame_torneo.grid_rowconfigure(0, weight=1)
        self.frame_torneo.grid_rowconfigure(1, weight=1)
        self.frame_torneo.grid_rowconfigure(2, weight=1)
        self.frame_torneo.grid_rowconfigure(3, weight=1)

        tk.CTkButton(
            self.frame_torneo, text="go back", width=100,
            fg_color="transparent", border_width=1,
            command=self.volver
        ).grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.input_nombre = tk.CTkEntry(self.frame_torneo, placeholder_text="Nombre del Torneo", width=200)
        self.input_nombre.grid(row=0, column=1, pady=(40, 10))

        self.input_fecha_inicio = tk.CTkEntry(self.frame_torneo, placeholder_text="Fecha de Inicio DD/MM/AAAA", width=200)
        self.input_fecha_inicio.grid(row=1, column=1, pady=10)

        self.input_fecha_fin = tk.CTkEntry(self.frame_torneo, placeholder_text="Fecha de Final DD/MM/AAAA", width=200)
        self.input_fecha_fin.grid(row=2, column=1, pady=10)

        tk.CTkButton(
            self.frame_torneo, text="Guardar Torneo", width=200,
            fg_color="#29ABE2",
            command=self.guardar_data_torneo
        ).grid(row=3, column=1, pady=(20, 10))

        tk.CTkButton(
            self.frame_torneo, text="Grupos ->", width=110,
            fg_color="#29ABE2", border_width=0,
            command=self.go_to_grupos
        ).grid(row=2, column=2, padx=20, sticky="e")



        # -----------------------------------------------------------------------------------------------

        """aca empieza la pagina 2 o vista 2 idk es lo de los grupos"""
        
        # frame 2, se crea sendo transparente para que no se muestre hasta que se toque
        # el boton de Grupos ->
        self.frame_grupos = tk.CTkFrame(self, fg_color="transparent")
        # no se hace grid todavia, se muestra solo cuando se llama go_to_grupos

        self.frame_grupos.grid_columnconfigure(0, weight=1)
        self.frame_grupos.grid_columnconfigure(1, weight=2)
        self.frame_grupos.grid_columnconfigure(2, weight=1)
        self.frame_grupos.grid_rowconfigure(0, weight=1)
        self.frame_grupos.grid_rowconfigure(1, weight=1)
        self.frame_grupos.grid_rowconfigure(2, weight=1)
        self.frame_grupos.grid_rowconfigure(3, weight=1)

        tk.CTkButton(
            self.frame_grupos, text="<- Torneo", width=100,
            fg_color="transparent", border_width=1,
            command=self.go_to_torneo
        ).grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # Por aca tienen que estar los campos 
        tk.CTkLabel(self.frame_grupos, text="Configuración de Grupos").grid(row=0, column=1, pady=(40, 10))

        

        tk.CTkButton(
            self.frame_grupos, text="Guardar Grupos", width=200,
            fg_color="#29ABE2",
            command=self.guardar_grupos
        ).grid(row=3, column=1, pady=(20, 10))

        tk.CTkButton(
            self.frame_grupos, text="Equipos ->", width=110,
            fg_color="transparent", border_width=0,
            command=lambda: None  # proxima vista
        ).grid(row=2, column=2, padx=20, sticky="e")




    #----------------------------------------------------------------------------------------------------------
    """vista 3 por aca"""

    # esta es la funcion para cambiar de pagina
    def go_to_grupos(self):
        # grid remove borra el grid pero no el frame, entonces podes llamar grid otra vez para volver a mostrar
        self.frame_torneo.grid_remove()
        # se habilita el grid
        self.frame_grupos.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

    def go_to_torneo(self):
        self.frame_grupos.grid_remove()
        self.frame_torneo.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

    def guardar_data_torneo(self):
        nombre = self.input_nombre.get().strip()
        fecha_inicio = self.input_fecha_inicio.get().strip()
        fecha_fin = self.input_fecha_fin.get().strip()

        if not nombre or not fecha_inicio or not fecha_fin:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return

        try:
            dt_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            dt_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        except ValueError:
            CTkMessagebox(title="Error", message="Formato de fecha invalido, usa DD/MM/AAAA", icon="cancel")
            return

        hoy = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        if dt_inicio < hoy:
            CTkMessagebox(title="Error", message="La fecha de inicio no puede ser anterior a hoy", icon="cancel")
            return

        if dt_fin <= dt_inicio:
            CTkMessagebox(title="Error", message="La fecha de fin debe ser posterior a la de inicio", icon="cancel")
            return

        cargarTorneo(nombre, fecha_inicio, fecha_fin)
        CTkMessagebox(title="Exito", message="Torneo guardado correctamente", icon="check")

    def guardar_grupos(self):
        pass

    def cerrar_config(self):
        self.main_frame.habilitar_botones()
        self.root.back_to_main(self)

    def volver(self):
        self.root.back_to_main(self)